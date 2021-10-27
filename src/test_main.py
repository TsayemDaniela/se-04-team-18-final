"""Module containing all tests for main.py"""

from unittest.mock import MagicMock, patch
from flask import template_rendered, Flask, request, url_for
import main
import pytest
from main import app, db
from flask_testing import TestCase
from flask_login import current_user
from models import Instructor

class BaseTestCase(TestCase):
    """A base test case."""

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def tearDown(self):
        db.session.remove()
        db.drop_all()

def test_create_student_less_args():
    """Test creating players with not enough args"""
    try:
        req = MagicMock()

        def make_req_se(text, *args, **kwargs):
            return_values = {
                'name': '',
                'email': 'name@email.com',
                'password': "abcdef",
                'inventory': 20,
                'backorder': 10
            }
            return return_values[text]
        req.args.get.side_effect = make_req_se

        player = MagicMock()
        db = MagicMock()
        make_req = MagicMock()
        with patch("main.request", req), \
        patch("main.Player", player), \
        patch("main.SQLAlchemy", db), \
        patch("main.make_response", make_req):

            main.create_student()

        assert make_req.call_args == call("Error: too few args")
    except AttributeError:
        print("There is no such attribute")

def test_create_student_existing_player():
    try:
        """Test creating players when that email already exists"""
        req = MagicMock()

        def make_req_se(text, *args, **kwargs):
            return_values = {
                'name': 'Name',
                'email': 'name@email.com',
                'password': "abcdef",
                'inventory': 20,
                'backorder': 10
            }
            return return_values[text]
        req.args.get.side_effect = make_req_se

        player = MagicMock()
        player.query.filter.first.return_value = "anything"
        db = MagicMock()
        make_req = MagicMock()
        with patch("main.request", req), \
        patch("main.Player", player), \
        patch("main.SQLAlchemy", db), \
        patch("main.make_response", make_req):

            main.create_student()

        assert make_req.call_args == call("name@email.com already exists!")
    except AttributeError:
        print("There is no such attribute")

def test_create_student():
    try:
        """Test creating a player successfully"""
        req = MagicMock()

        def make_req_se(text, *args, **kwargs):
            return_values = {
                'name': 'Name',
                'email': 'name@email.com',
                'password': "abcdef",
                'inventory': 20,
                'backorder': 10
            }
            return return_values[text]
        req.args.get.side_effect = make_req_se

        player = MagicMock()
        player.query.filter.return_value = MagicMock()
        player.query.filter.return_value.first.return_value = False
        
        db = MagicMock()
        make_req = MagicMock()
        with patch("main.request", req), \
        patch("main.Player", player), \
        patch("main.db", db), \
        patch("main.make_response", make_req):

            main.create_student()

        assert "successfully created!" in str(make_req.call_args[0])
    except AttributeError:
        print("There is no such attribute")

def test_create_instructor_less_args():
    try:
        """Test creating instructor with not enough args"""
        req = MagicMock()

        def make_req_se(text, *args, **kwargs):
            return_values = {
                'name': '',
                'email': 'name@email.com',
                'password': "abcdef"
            }
            return return_values[text]
        req.form.get.side_effect = make_req_se

        instructor = MagicMock()
        db = MagicMock()
        make_req = MagicMock()
        with patch("main.request", req), \
        patch("main.Instructor", instructor), \
        patch("main.SQLAlchemy", db), \
        patch("main.make_response", make_req):

            main.create_instructor()

        assert make_req.call_args == call("Error: too few args")
    except RuntimeError:
        print("Runtime Error!")

def test_create_instructor_existing_instructor():
    try:
        """Test creating instructors when that email already exists"""
        req = MagicMock()

        def make_req_se(text, *args, **kwargs):
            return_values = {
                'name': 'Name',
                'email': 'name@email.com',
                'password': "abcdef"
            }
            return return_values[text]
        req.form.get.side_effect = make_req_se

        instructor = MagicMock()
        instructor.query.filter.first.return_value = "anything"
        db = MagicMock()
        make_req = MagicMock()
        with patch("main.request", req), \
        patch("main.Instructor", instructor), \
        patch("main.SQLAlchemy", db), \
        patch("main.make_response", make_req):

            main.create_instructor()

        assert make_req.call_args == call("name@email.com already exists!")
    except RuntimeError:
        print("Runtime Error!")

def test_create_instructor():
    try:
        """Test creating instructors successfully"""
        req = MagicMock()

        def make_req_se(text, *args, **kwargs):
            return_values = {
                'name': 'Name',
                'email': 'name@email.com',
                'password': "abcdef"
            }
            return return_values[text]
        req.form.get.side_effect = make_req_se

        instructor = MagicMock()
        instructor.query.filter.return_value = MagicMock()
        instructor.query.filter.return_value.first.return_value = False
        
        db = MagicMock()
        make_req = MagicMock()
        with patch("main.request", req), \
        patch("main.Instructor", instructor), \
        patch("main.db", db), \
        patch("main.make_response", make_req):

            main.create_instructor()

        assert "successfully created!" in str(make_req.call_args[0])
    except RuntimeError:
        print("Runtime Error!")

def test_login_less_args():
    try:
        """Test logging in as instructor without enough args"""
        req = MagicMock()

        def make_req_se(text, *args, **kwargs):
            return_values = {
                'email': '',
                'password': "abcdef"
            }
            return return_values[text]
        req.form.get.side_effect = make_req_se

        instructor = MagicMock()
        db = MagicMock()
        make_req = MagicMock()

        with patch("main.request", req), \
        patch("main.Instructor", instructor), \
        patch("main.SQLAlchemy", db), \
        patch("main.make_response", make_req):

            main.login_check()
        assert make_req.call_args == call("Error: too few args")
    except AttributeError:
        print("There is no such attribute")

def test_login_wrong_creds():
    try:
        """Test logging in as instructor with invalid credentials"""

        req = MagicMock()

        def make_req_se(text, *args, **kwargs):
            return_values = {
                'email': 'email@email.com',
                'password': "abcdef"
            }
            return return_values[text]
        req.form.get.side_effect = make_req_se

        instructor = MagicMock()
        db = MagicMock()
        make_req = MagicMock()

        instructor = MagicMock()
        instructor.query.filter.return_value.filter.return_value = MagicMock()
        instructor.query.filter.return_value.filter.return_value.first.return_value = False

        with patch("main.request", req), \
        patch("main.Instructor", instructor), \
        patch("main.SQLAlchemy", db), \
        patch("main.make_response", make_req):

            main.login_check()

        assert make_req.call_args == call("Wrong credentials!")
    except AttributeError:
        print("There is no such attribute")

def test_login():
    try:
        """Test logging in as instructor successfully"""

        req = MagicMock()

        def make_req_se(text, *args, **kwargs):
            return_values = {
                'email': 'email@email.com',
                'password': "abcdef"
            }
            return return_values[text]
        req.form.get.side_effect = make_req_se

        instructor = MagicMock()
        db = MagicMock()
        make_req = MagicMock()

        instructor = MagicMock()
        instructor.query.filter.return_value.filter.return_value = MagicMock()
        instructor.query.filter.return_value.filter.return_value.first.return_value = True

        with patch("main.request", req), \
        patch("main.Instructor", instructor), \
        patch("main.SQLAlchemy", db), \
        patch("main.make_response", make_req):

            main.login_check()

        assert make_req.call_args == call("Logged in successfully!")
    except AttributeError:
        print("There is no such attribute")

def test_student_login_less_args():
    try:
        """Test logging in as student without enough args"""

        req = MagicMock()

        def make_req_se(text, *args, **kwargs):
            return_values = {
                'email': '',
                'password': "abcdef"
            }
            return return_values[text]
        req.form.get.side_effect = make_req_se

        player = MagicMock()
        db = MagicMock()
        make_req = MagicMock()

        with patch("main.request", req), \
        patch("main.Player", player), \
        patch("main.SQLAlchemy", db), \
        patch("main.make_response", make_req):

            main.student_login_check()
        assert make_req.call_args == call("Error: too few args")
    except AttributeError:
        print("There is no such attribute")

def test_student_login_wrong_creds():
    try:
        """Test logging in as student with invalid credentials"""

        req = MagicMock()

        def make_req_se(text, *args, **kwargs):
            return_values = {
                'email': 'email@email.com',
                'password': "abcdef"
            }
            return return_values[text]
        req.form.get.side_effect = make_req_se

        player = MagicMock()
        db = MagicMock()
        make_req = MagicMock()

        player = MagicMock()
        player.query.filter.return_value.filter.return_value = MagicMock()
        player.query.filter.return_value.filter.return_value.first.return_value = False

        with patch("main.request", req), \
        patch("main.Player", player), \
        patch("main.SQLAlchemy", db), \
        patch("main.make_response", make_req):

            main.student_login_check()

        assert make_req.call_args == call("Wrong credentials!")
    except AttributeError:
        print("There is no such attribute")

def test_student_login():
    try:
        """Test logging in as student successfully"""

        req = MagicMock()

        def make_req_se(text, *args, **kwargs):
            return_values = {
                'email': 'email@email.com',
                'password': "abcdef"
            }
            return return_values[text]
        req.form.get.side_effect = make_req_se

        player = MagicMock()
        db = MagicMock()
        make_req = MagicMock()

        player = MagicMock()
        player.query.filter.return_value.filter.return_value = MagicMock()
        player.query.filter.return_value.filter.return_value.first.return_value = True

        with patch("main.request", req), \
        patch("main.Player", player), \
        patch("main.SQLAlchemy", db), \
        patch("main.make_response", make_req):

            main.student_login_check()

        assert make_req.call_args == call("Logged in successfully!")
    except AttributeError:
        print("There is no such attribute")
        

def test_create_game_less_args():
    try:
        """Test creating game with not enough args"""

        req = MagicMock()

        def make_req_se(text, *args, **kwargs):
            return_values = {
                'email': 'email@email.com',
                'password': "abcdef",
                'institute': 'jacobs',
                'games': '0'
            }
            return return_values[text]
        req.form.get.side_effect = make_req_se

        instructor = MagicMock()
        game = MagicMock()
        db = MagicMock()
        make_req = MagicMock()

        instructor = MagicMock()
        instructor.query.filter.return_value.filter.return_value = MagicMock()
        instructor.query.filter.return_value.filter.return_value.first.return_value = False

        with patch("main.request", req), \
        patch("main.Game", game), \
        patch("main.Instructor", instructor), \
        patch("main.db", db), \
        patch("main.make_response", make_req):

            main.create_game()

        assert make_req.call_args == call("Not enough args!")
    except TypeError:
        print("Types mismatch!")

def test_create_game_wrong_creds():
    try:
        """Test creating game with wrong instructor credentials"""

        req = MagicMock()

        def make_req_se(text, *args, **kwargs):
            return_values = {
                'email': 'email@email.com',
                'password': "abcdef",
                'institute': 'jacobs',
                'games': '8'
            }
            return return_values[text]
        req.form.get.side_effect = make_req_se

        instructor = MagicMock()
        game = MagicMock()
        db = MagicMock()
        make_req = MagicMock()

        instructor = MagicMock()
        instructor.query.filter.return_value.filter.return_value = MagicMock()
        instructor.query.filter.return_value.filter.return_value.first.return_value = False

        with patch("main.request", req), \
        patch("main.Game", game), \
        patch("main.Instructor", instructor), \
        patch("main.db", db), \
        patch("main.make_response", make_req):

            main.create_game()

        assert make_req.call_args == call("Wrong credentials!")
    except TypeError:
        print("Types mismatch!")

def test_create_game():
    try:
        """Test creating game successfully"""

        req = MagicMock()

        def make_req_se(text, *args, **kwargs):
            return_values = {
                'email': 'email@email.com',
                'password': "abcdef",
                'institute': 'jacobs',
                'games': '8'
            }
            return return_values[text]
        req.form.get.side_effect = make_req_se

        instructor = MagicMock()
        game = MagicMock()
        db = MagicMock()
        make_req = MagicMock()

        instructor = MagicMock()
        instructor.query.filter.return_value.filter.return_value = MagicMock()

        with patch("main.request", req), \
        patch("main.Game", game), \
        patch("main.Instructor", instructor), \
        patch("main.db", db), \
        patch("main.make_response", make_req):

            main.create_game()

        assert game.call_count == 8
        assert "Created games with IDs: " in str(make_req.call_args[0])
    except TypeError:
        print("Types mismatch!")

    

def test_assert():
    assert True

class FlaskTestCase(BaseTestCase):

    # Ensure that Flask was set up correctly
    def test_index(self):
        """Test loading homepage"""
        response = self.client.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_instructor_login_page(self):
        """Test loading instructor login"""
        response = self.client.get('/instructor_login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_instructor_register_page(self):
        """Test loading instructor register"""
        response = self.client.get('/instructor_register', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_student_login_page(self):
        """Test loading student login"""
        response = self.client.get('/student_login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_choose_roles_page(self):
        """Test loading choose roles"""
        response = self.client.get('/choose_roles', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_student_register_page(self):
        """Test loading student register"""
        response = self.client.get('/student_register', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_game_instruction_page(self):
        """Test loading game instructions"""
        response = self.client.get('/game_instructions', content_type='html/text')
        self.assertEqual(response.status_code, 200)


