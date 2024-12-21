from PIL import Image
import os

def create_icon_set(input_image_path, output_folder):
    """Tek bir yüksek çözünürlüklü PNG'den tüm gerekli boyutları oluşturur."""
    
    # Output klasörünü oluştur
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Gerekli boyutlar ve dosya isimleri
    sizes = [
        (16, 16, "icon_16x16.png"),
        (32, 32, "icon_16x16@2x.png"),
        (32, 32, "icon_32x32.png"),
        (64, 64, "icon_32x32@2x.png"),
        (128, 128, "icon_128x128.png"),
        (256, 256, "icon_128x128@2x.png"),
        (256, 256, "icon_256x256.png"),
        (512, 512, "icon_256x256@2x.png"),
        (512, 512, "icon_512x512.png"),
        (1024, 1024, "icon_512x512@2x.png")
    ]
    
    # Ana görüntüyü yükle
    with Image.open(input_image_path) as img:
        # PNG formatına çevir (eğer değilse)
        if img.format != 'PNG':
            img = img.convert('RGBA')
        
        # Her boyut için yeni dosya oluştur
        for width, height, filename in sizes:
            resized_img = img.resize((width, height), Image.Resampling.LANCZOS)
            output_path = os.path.join(output_folder, filename)
            resized_img.save(output_path, 'PNG', optimize=True)
            print(f"Oluşturuldu: {filename}")

# Kullanım
input_image = "../assets/pin-code.png"  # 1024x1024 orijinal görseliniz
output_folder = "../password_generator.iconset"
create_icon_set(input_image, output_folder)