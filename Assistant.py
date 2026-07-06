import speech_recognition as sr
import datetime
import webbrowser
import os
import requests
import edge_tts
import asyncio
import pygame
import time
import subprocess

from config import close_apps
from whatsapp import send_whatsapp
from utils import clean_text, clean_command
