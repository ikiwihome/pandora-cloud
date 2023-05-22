# -*- coding: utf-8 -*-

import logging
from datetime import datetime
from os import getenv
from os.path import join, abspath, dirname

from flask import Flask, jsonify, request, render_template, redirect, url_for, make_response
from pandora_cloud.exts.hooks import hook_logging
from pandora_cloud.exts.token import check_access_token
from pandora_cloud.openai.auth import Auth0
from waitress import serve
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.serving import WSGIRequestHandler

from . import __version__


class ChatBot:
    __default_ip = '0.0.0.0'
    __default_port = 8080
    __build_id = '35uzIQibpwv56FyPcgmGz'

    def __init__(self, proxy, debug=False, sentry=False, login_local=False):
        self.proxy = proxy
        self.debug = debug
        self.sentry = sentry
        self.login_local = login_local
        self.log_level = logging.DEBUG if debug else logging.WARN
        self.api_prefix = getenv('CHATGPT_API_PREFIX', 'https://ai.fakeopen.com')

        hook_logging(level=self.log_level, format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
        self.logger = logging.getLogger('waitress')

    def run(self, bind_str, threads=8):
        host, port = self.__parse_bind(bind_str)

        resource_path = abspath(join(dirname(__file__), 'flask'))
        app = Flask(__name__, static_url_path='',
                    static_folder=join(resource_path, 'static'),
                    template_folder=join(resource_path, 'templates'))
        app.wsgi_app = ProxyFix(app.wsgi_app, x_port=1)
        app.after_request(self.__after_request)

        app.route('/api/auth/session')(self.session)
        app.route('/api/accounts/check')(self.check)
        app.route('/auth/logout')(self.logout)
        app.route('/_next/data/{}/index.json'.format(self.__build_id))(self.chat_info)
        app.route('/_next/data/{}/c/<conversation_id>.json'.format(self.__build_id))(self.chat_info)

        app.route('/')(self.chat)
        app.route('/c')(self.chat)
        app.route('/c/<conversation_id>')(self.chat)

        app.route('/chat')(self.chat_index)
        app.route('/chat/<conversation_id>')(self.chat_index)

        app.route('/auth/login')(self.login)
        app.route('/auth/login', methods=['POST'])(self.login_post)
        app.route('/auth/login_token', methods=['POST'])(self.login_token)

        if not self.debug:
            self.logger.warning('Serving on http://{}:{}'.format(host, port))

        WSGIRequestHandler.protocol_version = 'HTTP/1.1'
        serve(app, host=host, port=port, ident=None, threads=threads)

    @staticmethod
    def __after_request(resp):
        resp.headers['X-Server'] = 'pandora-cloud/{}'.format(__version__)

        return resp

    def __parse_bind(self, bind_str):
        sections = bind_str.split(':', 2)
        if len(sections) < 2:
            try:
                port = int(sections[0])
                return self.__default_ip, port
            except ValueError:
                return sections[0], self.__default_port

        return sections[0], int(sections[1])

    @staticmethod
    def __set_cookie(resp, token, expires):
        resp.set_cookie('access-token', token, expires=expires, path='/', domain=None, httponly=True, samesite='Lax')

    @staticmethod
    def __get_userinfo():
        access_token = request.cookies.get('access-token')
        try:
            payload = check_access_token(access_token)
            if 'https://api.openai.com/auth' not in payload or 'https://api.openai.com/profile' not in payload:
                raise Exception('invalid access token')
        except:
            return True, None, None, None, None

        user_id = payload['https://api.openai.com/auth']['user_id']
        email = payload['https://api.openai.com/profile']['email']

        return False, user_id, email, access_token, payload

    @staticmethod
    def chat_index(conversation_id=None):
        resp = redirect('/')

        return resp

    def logout(self):
        resp = redirect(url_for('login'))
        self.__set_cookie(resp, '', 0)

        return resp

    def login(self):
        return render_template('login.html', api_prefix=self.api_prefix)

    def login_post(self):
        username = request.form.get('username')
        password = request.form.get('password')
        error = None

        if username and password:
            try:
                access_token = Auth0(username, password, self.proxy).auth(self.login_local)
                payload = check_access_token(access_token)

                resp = make_response('please wait...', 302)
                resp.headers.set('Location', '/')
                self.__set_cookie(resp, access_token, payload['exp'])

                return resp
            except Exception as e:
                error = str(e)

        return render_template('login.html', username=username, error=error, api_prefix=self.api_prefix)

    def login_token(self):
        access_token = request.form.get('access_token')
        error = None

        if access_token:
            try:
                payload = check_access_token(access_token)

                resp = jsonify({'code': 0, 'url': '/'})
                self.__set_cookie(resp, access_token, payload['exp'])

                return resp
            except Exception as e:
                error = str(e)

        return jsonify({'code': 500, 'message': 'Invalid access token: {}'.format(error)})

    def chat(self, conversation_id=None):
        err, user_id, email, _, _ = self.__get_userinfo()
        if err:
            return redirect(url_for('login'))

        query = request.args.to_dict()
        if conversation_id:
            query['chatId'] = conversation_id

        props = {
            'props': {
                'pageProps': {
                    'user': {
                        'id': user_id,
                        'name': email,
                        'email': email,
                        'image': None,
                        'picture': None,
                        'groups': [],
                    },
                    'serviceStatus': {},
                    'userCountry': 'US',
                    'geoOk': True,
                    'serviceAnnouncement': {
                        'paid': {},
                        'public': {}
                    },
                    'isUserInCanPayGroup': True
                },
                '__N_SSP': True
            },
            'page': '/c/[chatId]' if conversation_id else '/',
            'query': query,
            'buildId': self.__build_id,
            'isFallback': False,
            'gssp': True,
            'scriptLoader': []
        }

        template = 'detail.html' if conversation_id else 'chat.html'
        return render_template(template, pandora_sentry=self.sentry, api_prefix=self.api_prefix, props=props)

    def session(self):
        err, user_id, email, access_token, payload = self.__get_userinfo()
        if err:
            return jsonify({})

        ret = {
            'user': {
                'id': user_id,
                'name': email,
                'email': email,
                'image': None,
                'picture': None,
                'groups': [],
            },
            'expires': datetime.utcfromtimestamp(payload['exp']).isoformat(),
            'accessToken': access_token,
            'authProvider': 'auth0',
        }

        return jsonify(ret)

    def chat_info(self, conversation_id=None):
        err, user_id, email, _, _ = self.__get_userinfo()
        if err:
            return jsonify({'pageProps': {'__N_REDIRECT': '/auth/login?', '__N_REDIRECT_STATUS': 307}, '__N_SSP': True})

        ret = {
            'pageProps': {
                'user': {
                    'id': user_id,
                    'name': email,
                    'email': email,
                    'image': None,
                    'picture': None,
                    'groups': [],
                },
                'serviceStatus': {},
                'userCountry': 'US',
                'geoOk': True,
                'serviceAnnouncement': {
                    'paid': {},
                    'public': {}
                },
                'isUserInCanPayGroup': True
            },
            '__N_SSP': True
        }

        return jsonify(ret)

    @staticmethod
    def check():
        ret = {
            'account_plan': {
                'is_paid_subscription_active': True,
                'subscription_plan': 'chatgptplusplan',
                'account_user_role': 'account-owner',
                'was_paid_customer': True,
                'has_customer_object': True,
                'subscription_expires_at_timestamp': 3774355199
            },
            'user_country': 'US',
            'features': [
                'model_switcher',
                'model_preview',
                'system_message',
                'can_continue',
                'data_controls_enabled',
                'data_export_enabled',
                'show_existing_user_age_confirmation_modal',
                'bucketed_history',
                'priority_driven_models_list',
                'message_style_202305',
                'layout_may_2023',
                'plugins_available',
                'beta_features',
                'infinite_scroll_history',
                'browsing_available',
                'browsing_inner_monologue',
                'tools3_dev',
                'tools3_admin',
                'tools2',
                'debug',
            ],
        }

        return jsonify(ret)
