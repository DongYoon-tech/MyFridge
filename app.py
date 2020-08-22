from flask import Flask, render_template, request, flash, redirect, session, g, abort
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

@app.route('/')
def home():
    """Home page"""
    return render_template('index.html')