import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QLabel, QLineEdit, QPushButton, QMessageBox, QTableWidget,
                           QTableWidgetItem, QHeaderView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap
import random
import string

class PasswordViewer(QMainWindow):
    """Kaydedilmiş şifreleri görüntülemek için kullanılan pencere sınıfı"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kayıtlı Şifreler")
        self.setFixedSize(600, 400)
        
        # Ana widget ve layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Arama alanı
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Şifre ismine göre ara...")
        self.search_input.textChanged.connect(self.filter_passwords)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # Şifre tablosu
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Şifre İsmi", "Şifre", "Kopyala"])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(2, 100)
        layout.addWidget(self.table)
        
        # Alt butonlar
        button_layout = QHBoxLayout()
        refresh_button = QPushButton("Yenile")
        refresh_button.clicked.connect(self.load_passwords)
        delete_button = QPushButton("Seçili Şifreyi Sil")
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
            self.table.setHorizontalHeaderLabels(["Şifre İsmi", "Şifre", "", ""])
            
            # Sütun genişliklerini ayarla
            header = self.table.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
            header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
            self.table.setColumnWidth(2, 40)
            self.table.setColumnWidth(3, 40)
            
            with open('passwords.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    if ':' in line:
                        name, password = line.strip().split(':', 1)
                        row_position = self.table.rowCount()
                        self.table.insertRow(row_position)
                        
                        # Şifre ismi
                        self.table.setItem(row_position, 0, QTableWidgetItem(name))
                        
                        # Şifre (gizli)
                        password_item = QTableWidgetItem('*' * len(password))
                        password_item.setData(Qt.ItemDataRole.UserRole, password)
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
            msg.setText("Şifre panoya kopyalandı!")
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
            reply = QMessageBox.question(self, 'Silme Onayı', 
                                       'Seçili şifreyi silmek istediğinize emin misiniz?',
                                       QMessageBox.StandardButton.Yes |
                                       QMessageBox.StandardButton.No)
            
            if reply == QMessageBox.StandardButton.Yes:
                name_item = self.table.item(current_row, 0)
                if name_item:
                    name = name_item.text()
                    # Dosyadan şifreyi sil
                    with open('passwords.txt', 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    with open('passwords.txt', 'w', encoding='utf-8') as f:
                        for line in lines:
                            if not line.startswith(f"{name}:"):
                                f.write(line)
                    # Tablodan satırı kaldır
                    self.table.removeRow(current_row)
                    QMessageBox.information(self, "Başarılı", "Şifre silindi!")
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen silmek istediğiniz şifreyi seçin.")
 
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
         
        icon_path = resource_path(os.path.join('assets', 'pin-code.png'))
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            
        self.setWindowTitle("Otomatik Şifre Üretici")
        self.setFixedSize(400, 400)
        
        # Ana widget ve layout oluşturma
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Şifre ismi için alan ekleme
        self.password_name_label = QLabel("Şifre İsmi (Websitesi/Uygulama):")
        self.password_name_input = QLineEdit()
        self.password_name_input.setPlaceholderText("Örnek: Gmail, Instagram, Netflix...")
        
        # Diğer arayüz elemanlarını oluşturma
        self.length_label = QLabel("Şifre Uzunluğu:")
        self.length_input = QLineEdit()
        
        self.letter_label = QLabel("Harf Sayısı:")
        self.letter_input = QLineEdit()
        
        self.number_label = QLabel("Rakam Sayısı (Opsiyonel):")
        self.number_input = QLineEdit()
        
        self.special_char_label = QLabel("Özel Karakter Sayısı (Opsiyonel):")
        self.special_char_input = QLineEdit()
        
        self.special_char_pool_label = QLabel("Özel Karakter Havuzu (Opsiyonel):")
        self.special_char_pool_input = QLineEdit()
        self.special_char_pool_input.setText("@#$%&*")
        
        self.generate_button = QPushButton("Şifre Oluştur")
        self.generate_button.clicked.connect(self.generate_password)
        
         # Şifre görüntüleme butonu
        self.view_passwords_button = QPushButton("Kayıtlı Şifreleri Görüntüle")
        self.view_passwords_button.clicked.connect(self.show_password_viewer)
        
        self.result_label = QLabel("Oluşturulan Şifre: Henüz oluşturulmadı.")
        
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

    def show_password_viewer(self):
        """Şifre görüntüleyici penceresini açar"""
        self.password_viewer = PasswordViewer()
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
            QMessageBox.warning(self, "Hata", str(e))
        except Exception as e:
            QMessageBox.warning(self, "Hata", "Lütfen geçerli sayısal değerler girin.")

    def ask_to_save(self, password):
        # Şifre ismi boş ise uyarı ver
        password_name = self.password_name_input.text().strip()
        if not password_name:
            reply = QMessageBox.question(self, 'Uyarı', 
                                       'Şifre ismi girilmedi. Yine de kaydetmek ister misiniz?',
                                       QMessageBox.StandardButton.Yes |
                                       QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.No:
                return
        
        reply = QMessageBox.question(self, 'Kaydet', 
                                   'Şifreyi kaydetmek ister misiniz?',
                                   QMessageBox.StandardButton.Yes |
                                   QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                with open('passwords.txt', 'a', encoding='utf-8') as f:
                    # Şifre ismini ve şifreyi kaydet
                    save_line = f"{password_name}:{password}\n" if password_name else f"Adsız:{password}\n"
                    f.write(save_line)
                QMessageBox.information(self, "Başarılı", "Şifre kaydedildi!")
                
                # Başarılı kayıttan sonra şifre ismi alanını temizle
                self.password_name_input.clear()
            except Exception as e:
                QMessageBox.warning(self, "Hata", f"Şifre kaydedilemedi: {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = PasswordGenerator()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()