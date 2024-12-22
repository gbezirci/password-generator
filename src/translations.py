TRANSLATIONS = {
    'en_US': {
        'window_title': "Password Generator",
        'password_name_label': "Password Name (Website/App):",
        'password_name_placeholder': "Example: Gmail, Instagram, Netflix...",
        'length_label': "Password Length:",
        'letter_label': "Number of Letters:",
        'number_label': "Number of Digits (Optional):",
        'special_char_label': "Number of Special Characters (Optional):",
        'special_char_pool_label': "Special Character Pool (Optional):",
        'generate_button': "Generate Password",
        'view_passwords_button': "View Saved Passwords",
        'result_label': "Generated Password: Not generated yet.",
        'save_question': "Do you want to save the password?",
        'save_success': "Password saved successfully! 🎉",
        'save_error': "Could not save password: {}",
        'warning': "Warning",
        'error': "Error",
        'success': "Success",
        'error_detail_1': "Please enter valid numerical values.",
        'save': "Save",
        'password_name_warning': "Password name not entered. Do you still want to save?",
        'search_pass_placeholder': "Search by password name...",
        'pass_name': "Password Name",
        'pass': "Password",
        'delete': "Delete",
        'copy': "Copy",
        'refresh': "Refresh",
        'selected_pass_remove': "Delete selected password",
        'selected_pass_copyed': "Selected password copied",
        'del_approv': "Delete Confirmation",
        'del_approv_text': "Are you sure you want to delete the selected password?",
        'pass_deleted': "Password deleted",
        'please_select_delete_pass': "Please select a password to delete"
    },
    'tr_TR': {
        'window_title': "Şifre Üretici",
        'password_name_label': "Şifre İsmi (Websitesi/Uygulama):",
        'password_name_placeholder': "Örnek: Gmail, Instagram, Netflix...",
        'length_label': "Şifre Uzunluğu:",
        'letter_label': "Harf Sayısı:",
        'number_label': "Rakam Sayısı (Opsiyonel):",
        'special_char_label': "Özel Karakter Sayısı (Opsiyonel):",
        'special_char_pool_label': "Özel Karakter Havuzu (Opsiyonel):",
        'generate_button': "Şifre Oluştur",
        'view_passwords_button': "Kayıtlı Şifreleri Görüntüle",
        'result_label': "Oluşturulan Şifre: Henüz oluşturulmadı.",
        'save_question': "Şifreyi kaydetmek ister misiniz?",
        'save_success': "Şifre kaydedildi! 🎉",
        'save_error': "Şifre kaydedilemedi: {}",
        'warning': "Uyarı",
        'error': "Hata",
        'success': "Başarılı",
        'error_detail_1': "Lütfen geçerli sayısal değerler girin.",
        'save': "Kaydet",
        'password_name_warning': "Şifre ismi girilmedi. Yine de kaydetmek ister misiniz?",
        'search_pass_placeholder': "Şifre ismine göre ara...",
        'pass_name': "Şifre İsmi",
        'pass': "Şifre",
        'delete': "Sil",
        'copy': "Kopyala",
        'refresh': "Yenile",
        'selected_pass_remove': "Seçilen şifreyi sil",
        'selected_pass_copyed': "Seçilen şifre kopyalandı",
        'del_approv': "Silme Onayı",
        'del_approv_text': "Seçilen şifreyi silmek istediğinizden emin misiniz?",
        'pass_deleted': "Şifre silindi",
        'please_select_delete_pass': "Lütfen silmek istediğiniz şifreyi seçin"
    }
}

def get_system_language():
    """Sistem dilini al ve desteklenen dillere eşle"""
    import locale
    system_locale, _ = locale.getdefaultlocale()
    
    # Desteklenen diller
    supported_languages = {
        'en_US': 'en_US',
        'tr_TR': 'tr_TR',
        # Diğer diller buraya eklenebilir
    }
    
    return supported_languages.get(system_locale, 'en_US')

def get_translations():
    """Sistem diline göre çevirileri döndür"""
    language = get_system_language()
    return TRANSLATIONS.get(language, TRANSLATIONS['en_US'])
