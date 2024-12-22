import sys
import os
import random
import string
import stat
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QLabel, QLineEdit, QPushButton, QMessageBox, QTableWidget,
                           QTableWidgetItem, QHeaderView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap
from cryptography.fernet import Fernet
from translations import get_translations

class PasswordViewer(QMainWindow):
    """Kaydedilmiş şifreleri görüntülemek için kullanılan pencere sınıfı"""
    def __init__(self, password_file_path, cipher):
        super().__init__()
        
         # Çevirileri yükle
        self.tr = get_translations()
        
        self.setWindowTitle(self.tr['view_passwords_button'])
        self.setFixedSize(600, 400)
        
         # Şifre dosyasının yolu
        self.password_file_path = password_file_path
        self.cipher = cipher
        
        # Ana widget ve layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Arama alanı
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(self.tr['search_pass_placeholder'])
        self.search_input.textChanged.connect(self.filter_passwords)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # Şifre tablosu
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels([self.tr["pass_name"], self.tr["pass"], self.tr["copy"]])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(2, 100)
        layout.addWidget(self.table)
        
        # Alt butonlar
        button_layout = QHBoxLayout()
        refresh_button = QPushButton(self.tr["refresh"])
        refresh_button.clicked.connect(self.load_passwords)
        delete_button = QPushButton(self.tr["selected_pass_remove"])
        delete_button.clicked.connect(self.delete_selected_password)
        button_layout.addWidget(refresh_button)
        button_layout.addWidget(delete_button)
        layout.addLayout(button_layout)
        
        # Şifreleri yükle
        self.load_passwords()

    def load_passwords(self):
        """Kayıtlı şifreleri dosyadan okur ve tabloya yükler."""
        try:
            self.table.setRowCount(0)
            self.table.setColumnCount(4)  # Bir sütun daha ekliyoruz
            self.table.setHorizontalHeaderLabels([self.tr["pass_name"], self.tr["pass"], "", ""])
            
            # Sütun genişliklerini ayarla
            header = self.table.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
            header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
            self.table.setColumnWidth(2, 40)
            self.table.setColumnWidth(3, 40)
            
            with open(self.password_file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if ':' in line:
                        name, encrypted_password = line.strip().split(':', 1)
                        
                        # Şifreyi çöz
                        try:
                            decrypted_password = self.cipher.decrypt(encrypted_password.encode('utf-8')).decode('utf-8')
                        except Exception as e:
                            decrypted_password = "[HATA: Çözülemiyor]"
                        
                        row_position = self.table.rowCount()
                        self.table.insertRow(row_position)
                        
                        # Şifre ismi
                        self.table.setItem(row_position, 0, QTableWidgetItem(name))
                        
                        # Şifre (gizli)
                        password_item = QTableWidgetItem('*' * len(decrypted_password))
                        password_item.setData(Qt.ItemDataRole.UserRole, decrypted_password)
                        self.table.setItem(row_position, 1, password_item)
                        
                        # Göster/Gizle butonu
                        toggle_button = QPushButton("👁")
                        toggle_button.setFixedWidth(40)
                        toggle_button.setStyleSheet("""
                            QPushButton {
                                border: none;
                                background-color: transparent;
                                font-size: 20px;
                            }
                            QPushButton:hover {
                                background-color: rgba(255, 255, 255, 0.1);
                            }
                        """)
                        toggle_button.clicked.connect(lambda checked, row=row_position: self.toggle_password_visibility(row))
                        self.table.setCellWidget(row_position, 2, toggle_button)
                        
                        # Kopyala butonu
                        copy_button = QPushButton("📋")
                        copy_button.setFixedWidth(40)
                        copy_button.setStyleSheet("""
                            QPushButton {
                                border: none;
                                background-color: transparent;
                                font-size: 20px;
                            }
                            QPushButton:hover {
                                background-color: rgba(255, 255, 255, 0.1);
                            }
                        """)
                        copy_button.clicked.connect(lambda checked, row=row_position: self.copy_password(row))
                        self.table.setCellWidget(row_position, 3, copy_button)
        except FileNotFoundError:
            QMessageBox.information(self, "Bilgi", "Henüz kaydedilmiş şifre bulunmuyor.")
    
    def filter_passwords(self):
        """Şifreleri arama kutusuna göre filtreler."""
        search_text = self.search_input.text().lower()
        for row in range(self.table.rowCount()):
            name_item = self.table.item(row, 0)
            if name_item:
                name = name_item.text().lower()
                self.table.setRowHidden(row, search_text not in name)
    
    def copy_password(self, row):
        """Seçili şifreyi panoya kopyalar."""
        password_item = self.table.item(row, 1)
        if password_item:
            # Şifreyi panoya kopyala
            password = password_item.data(Qt.ItemDataRole.UserRole)
            clipboard = QApplication.clipboard()
            clipboard.setText(password)
            
            # Özel mesaj kutusu oluştur
            msg = QMessageBox(self)
            msg.setWindowTitle(" ")  # Boş başlık
            msg.setText(self.tr["selected_pass_copyed"])
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.setIconPixmap(QPixmap("./assets/msg-box-icos/copy.png"))
            
            # Stil tanımlaması
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: #2b2b2b;
                    border-radius: 10px;
                }
                QMessageBox QLabel {
                    color: white;
                    font-size: 14px;
                    padding: 20px 10px;
                }
                QPushButton {
                    background-color: #0d6efd;
                    color: white;
                    border: none;
                    padding: 8px 20px;
                    border-radius: 5px;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #0b5ed7;
                }
            """)
            
            msg.exec()
        
    def toggle_password_visibility(self, row):
        """Şifre görünürlüğünü değiştirir."""
        password_item = self.table.item(row, 1)
        if password_item:
            real_password = password_item.data(Qt.ItemDataRole.UserRole)
            current_text = password_item.text()
            
            if current_text == '*' * len(real_password):
                # Şifreyi göster
                password_item.setText(real_password)
                toggle_button = self.table.cellWidget(row, 2)
                toggle_button.setText("👁️‍🗨️")  # Farklı bir göz ikonu
            else:
                # Şifreyi gizle
                password_item.setText('*' * len(real_password))
                toggle_button = self.table.cellWidget(row, 2)
                toggle_button.setText("👁")
    
    def delete_selected_password(self):
        """Seçili şifreyi siler."""
        current_row = self.table.currentRow()
        if current_row >= 0:
            reply = QMessageBox.question(self, self.tr["del_approv"], 
                                       self.tr["del_approv_text"],
                                       QMessageBox.StandardButton.Yes |
                                       QMessageBox.StandardButton.No)
            
            if reply == QMessageBox.StandardButton.Yes:
                name_item = self.table.item(current_row, 0)
                if name_item:
                    name = name_item.text()
                    # Dosyadan şifreyi sil
                    with open(self.password_file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    with open(self.password_file_path, 'w', encoding='utf-8') as f:
                        for line in lines:
                            if not line.startswith(f"{name}:"):
                                f.write(line)
                    # Tablodan satırı kaldır
                    self.table.removeRow(current_row)
                    QMessageBox.information(self, self.tr["success"], self.tr["pass_deleted"])
        else:
            QMessageBox.warning(self, self.tr["success"], self.tr["please_select_delete_pass"])
 
def resource_path(relative_path):
    """Kaynak dosyaların yolunu çözümler"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
            
class PasswordGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
         # Çevirileri yükle
        self.tr = get_translations()
        
        icon_path = resource_path(os.path.join('assets', 'pin-code.png'))
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            
        self.setWindowTitle(self.tr['window_title'])
        self.setFixedSize(400, 400)
        
        # Ana widget ve layout oluşturma
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Şifre ismi için alan ekleme
        self.password_name_label = QLabel(self.tr['password_name_label'])
        self.password_name_input = QLineEdit()
        self.password_name_input.setPlaceholderText(self.tr['password_name_placeholder'])
        
        # Diğer arayüz elemanlarını oluşturma
        self.length_label = QLabel(self.tr['length_label'])
        self.length_input = QLineEdit()
        
        self.letter_label = QLabel(self.tr['letter_label'])
        self.letter_input = QLineEdit()
        
        self.number_label = QLabel(self.tr['number_label'])
        self.number_input = QLineEdit()
        
        self.special_char_label = QLabel(self.tr['special_char_label'])
        self.special_char_input = QLineEdit()
        
        self.special_char_pool_label = QLabel(self.tr['special_char_pool_label'])
        self.special_char_pool_input = QLineEdit()
        self.special_char_pool_input.setText("@#$%&*")
        
        self.generate_button = QPushButton(self.tr['generate_button'])
        self.generate_button.clicked.connect(self.generate_password)
        
         # Şifre görüntüleme butonu
        self.view_passwords_button = QPushButton(self.tr['view_passwords_button'])
        self.view_passwords_button.clicked.connect(self.show_password_viewer)
        
        self.result_label = QLabel(self.tr['result_label'])
        
        # Layout'a elemanları ekleme
        layout.addWidget(self.password_name_label)
        layout.addWidget(self.password_name_input)
        layout.addWidget(self.length_label)
        layout.addWidget(self.length_input)
        layout.addWidget(self.letter_label)
        layout.addWidget(self.letter_input)
        layout.addWidget(self.number_label)
        layout.addWidget(self.number_input)
        layout.addWidget(self.special_char_label)
        layout.addWidget(self.special_char_input)
        layout.addWidget(self.special_char_pool_label)
        layout.addWidget(self.special_char_pool_input)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.result_label)
        layout.addWidget(self.view_passwords_button)
        
        # Boşluk ekleme
        layout.addStretch()
        
         # Şifreleme anahtarının yolu
        self.key_file_path = os.path.expanduser("~/Library/Containers/com.passworddemon.passwordgenerator/Data/key.key")
        self.setup_encryption_key()
        
        # Şifreleme motoru
        with open(self.key_file_path, 'rb') as key_file:
            self.cipher = Fernet(key_file.read())
        
        # Dosya yolunu belirleme (macOS sandbox uyumlu)
        self.app_data_path = os.path.expanduser("~/Library/Containers/com.passworddemon.passwordgenerator/Data")
        os.makedirs(self.app_data_path, exist_ok=True)
        self.password_file_path = os.path.join(self.app_data_path, "passwords.txt")

    def show_password_viewer(self):
        """Şifre görüntüleyici penceresini açar"""
        self.password_viewer = PasswordViewer(self.password_file_path, self.cipher)
        self.password_viewer.show()

    def calculate_remaining_length(self, total_length, letter_count, number_count, special_count):
        """Boş bırakılan alan için gereken karakter sayısını hesaplar."""
        filled_count = sum(x for x in [letter_count, number_count, special_count] if x is not None)
        return total_length - filled_count if filled_count <= total_length else 0

    def generate_password(self):
        try:
            # Kullanıcı girişlerini alma
            total_length = int(self.length_input.text())
            
            # Girilen değerleri kontrol et ve boş olanları None olarak işaretle
            try:
                letter_count = int(self.letter_input.text()) if self.letter_input.text() else None
            except ValueError:
                letter_count = None
                
            try:
                number_count = int(self.number_input.text()) if self.number_input.text() else None
            except ValueError:
                number_count = None
                
            try:
                special_count = int(self.special_char_input.text()) if self.special_char_input.text() else None
            except ValueError:
                special_count = None
            
            # Dolu olan alanların toplamını hesapla
            filled_values = [x for x in [letter_count, number_count, special_count] if x is not None]
            filled_sum = sum(filled_values)
            
            # Toplam uzunluk kontrolü ve otomatik tamamlama
            if filled_sum > total_length:
                raise ValueError("Karakter sayıları toplamı şifre uzunluğundan fazla!")
            
            # Boş alanları otomatik doldur
            if letter_count is None and number_count is not None and special_count is not None:
                letter_count = total_length - (number_count + special_count)
            elif number_count is None and letter_count is not None and special_count is not None:
                number_count = total_length - (letter_count + special_count)
            elif special_count is None and letter_count is not None and number_count is not None:
                special_count = total_length - (letter_count + number_count)
            else:
                # Birden fazla alan boşsa, önceliği harflere ver
                remaining = total_length - filled_sum
                if letter_count is None:
                    letter_count = remaining if number_count is not None and special_count is not None else remaining // 2
                    remaining -= letter_count
                if number_count is None and remaining > 0:
                    number_count = remaining if special_count is not None else remaining // 2
                    remaining -= number_count
                if special_count is None and remaining > 0:
                    special_count = remaining
            
            # Karakter havuzlarını oluşturma
            letters = string.ascii_letters
            numbers = string.digits
            special_chars = self.special_char_pool_input.text() or "@#$%&*"
            
            # Şifreyi oluşturma
            password_chars = []
            password_chars.extend(random.choices(letters, k=letter_count))
            password_chars.extend(random.choices(numbers, k=number_count))
            password_chars.extend(random.choices(special_chars, k=special_count))
            
            # Karakterleri karıştırma
            random.shuffle(password_chars)
            password = ''.join(password_chars)
            
            # Sonucu gösterme
            self.result_label.setText(f"Oluşturulan Şifre: {password}")
            
            # Kaydetme seçeneği sunma
            self.ask_to_save(password)
            
        except ValueError as e:
            QMessageBox.warning(self, self.tr["error"], str(e))
        except Exception as e:
            QMessageBox.warning(self, self.tr["error"], self.tr["error_detail_1"])
    
    def setup_encryption_key(self):
        """Şifreleme için gerekli anahtarı oluşturur ve güvenli bir şekilde saklar."""
        if not os.path.exists(self.key_file_path):
            os.makedirs(os.path.dirname(self.key_file_path), exist_ok=True)
            with open(self.key_file_path, 'wb') as key_file:
                key_file.write(Fernet.generate_key())
            # Dosya izinlerini sadece kullanıcıya özel yap
            os.chmod(self.key_file_path, stat.S_IRUSR | stat.S_IWUSR)
            
    def ask_to_save(self, password):
        # Şifre ismi boş ise uyarı ver
        password_name = self.password_name_input.text().strip()
        if not password_name:
            reply = QMessageBox.question(self, self.tr['warning'], 
                                       self.tr['password_name_warning'],
                                       QMessageBox.StandardButton.Yes |
                                       QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.No:
                return
        
        reply = QMessageBox.question(self, self.tr['save'], 
                                   self.tr['save_question'],
                                   QMessageBox.StandardButton.Yes |
                                   QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                with open(self.password_file_path, 'a', encoding='utf-8') as f:
                    # Şifreyi şifrele ve dosyaya yaz
                    encrypted_password = self.cipher.encrypt(password.encode('utf-8'))
                    save_line = f"{password_name}:{encrypted_password.decode('utf-8')}\n" if password_name else f"Adsız:{encrypted_password.decode('utf-8')}\n"
                    f.write(save_line)
                QMessageBox.information(self, self.tr["success"], self.tr["save_success"])
                print(f"Dosya yolu: {self.password_file_path}")
                # Başarılı kayıttan sonra şifre ismi alanını temizle
                self.password_name_input.clear()
            except Exception as e:
                QMessageBox.warning(self, self.tr["error"], self.tr["save_error"])

def main():
    app = QApplication(sys.argv)
    window = PasswordGenerator()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()