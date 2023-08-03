from flask import Flask, render_template, request, flash, Blueprint
views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template("index.html")
