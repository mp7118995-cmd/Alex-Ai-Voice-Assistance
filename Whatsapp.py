import os
import time
import pyautogui
import pyperclip

from config import contacts

def send_whatsapp(command, speak):
   def send_whatsapp(command): 
  try: command = command.replace("alex", "").strip() 
       command = command.replace("send whatsapp", "").strip() 
       command = command.replace("whatsapp", "").strip() 
       command = command.replace("send message", "").strip() 
       command = command.replace("to", "", 1).strip() 

      print("Cleaned WhatsApp command:", command)
      words = command.split(" ", 1) 

      if len(words) < 2:   
        speak("Please say the contact name and then the message.") 
        return contact_name = words[0].strip() 
        message = words[1].strip() 
        
        if contact_name not in contacts: 
          speak(f"Contact {contact_name} not found.") 
          return full_name = contacts[contact_name]["name"] 
          speak(f"Sending message to {contact_name}.") 
         
          os.system("start whatsapp:") 
          time.sleep(4) 
         
          pyautogui.hotkey('ctrl', 'f') 
          time.sleep(0.5) 
         
          pyperclip.copy(full_name)
          pyautogui.hotkey('ctrl', 'v') 
          time.sleep(1.5) 
          
          pyautogui.press('enter')
          time.sleep(0.5) 
          
          pyperclip.copy(message) 
          pyautogui.hotkey('ctrl', 'v') 
          time.sleep(0.3)
          
          pyautogui.press('enter') 
          speak("Message sent.") 

  except Exception as e: 
  print("WhatsApp error:", e) 
  speak("Failed to send message.")
