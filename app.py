from flask import Flask, render_template, request
import re

# Definisikan DFA untuk pengecekan email
class DFA:
    def __init__(self):
        self.state = 'start'
        
    def reset(self):
        self.state = 'start'
    
    def transition(self, char):
        if self.state == 'start':
            if char.isalnum() or char in ['.', '_']:
                self.state = 'username'
                
        elif self.state == 'username':
            if char.isalnum() or char in ['.', '_']:
                self.state = 'username'
            elif char == '@':
                self.state = 'at'
                
        elif self.state == 'at':
            if char.isalnum():
                self.state = 'domain'
                
        elif self.state == 'domain':
            if char.isalnum():
                self.state = 'domain'
            elif char == '.':
                self.state = 'dot'
                
        elif self.state == 'dot':
            if char.isalnum():
                self.state = 'extension'
                
        elif self.state == 'extension':
            if char.isalnum():
                self.state = 'extension'
        
    
    def is_valid(self, email):
        self.reset()
        
        for char in email:
            self.transition(char)
            
        return self.state == 'extension'


# Fungsi untuk mengecek apakah email valid
def check_email_validity(email):
    dfa = DFA()
    return dfa.is_valid(email)


# Inisialisasi Flask
app = Flask(__name__)

# Halaman utama
@app.route("/", methods=["GET", "POST"])
def index():
    email = None
    is_valid = None

    if request.method == "POST":
        email = request.form["email"]
        is_valid = check_email_validity(email)

    return render_template("index.html", email=email, is_valid=is_valid)


# Menjalankan aplikasi Flask
if __name__ == "__main__":
    app.run(debug=True)
