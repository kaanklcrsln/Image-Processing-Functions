# Image Enhancement Filters Collection

Bu koleksiyon, Image_HW2.tif dosyası için kapsamlı görüntü iyileştirme filtrelerini içerir. Her filter farklı parametrelerle test edilmiş ve ayrı Python dosyalarında organize edilmiştir.

## Mevcut Filtreler

### 1. Kenar Geliştirme (Edge Enhancement)
- **`laplacian_enhancement.py`** - Laplacian kenar geliştirme
- **`sobel_enhancement.py`** - Sobel gradyan kenar geliştirme
- **`advanced_edge_filters.py`** - Canny, Prewitt, Roberts Cross filtreleri
- **`highpass_filter.py`** - Yüksek geçiren filtre

### 2. Gürültü Azaltma (Noise Reduction)
- **`gaussian_blur_filter.py`** - Gaussian bulanıklaştırma
- **`median_filter.py`** - Medyan filtresi (tuz-biber gürültüsü için)
- **`bilateral_filter.py`** - Kenar koruyucu yumuşatma

### 3. Kontrast Geliştirme (Contrast Enhancement)
- **`histogram_equalization.py`** - Histogram eşitleme
- **`adaptive_histogram_equalization.py`** - Uyarlanabilir histogram eşitleme (CLAHE)
- **`contrast_stretching.py`** - Doğrusal kontrast germe

### 4. Parlaklık Ayarı (Brightness Adjustment)
- **`gamma_log_transforms.py`** - Gamma düzeltme ve logaritmik dönüşüm

### 5. Keskinleştirme (Sharpening)
- **`highboost_unsharp.py`** - Unsharp masking
- **`highpass_filter.py`** - Yüksek frekans vurgulama

### 6. Pan-Keskinleştirme (Pansharpening)
- **`pansharpening_methods.py`** - Brovey, IHS, PCA yöntemleri

## Kullanım

### Tüm Filtreleri Çalıştırma
```bash
python run_all_filters.py
```

### Bireysel Filter Çalıştırma
```bash
python gaussian_blur_filter.py
python laplacian_enhancement.py
python histogram_equalization.py
# ... diğer filterler
```

## Filter Detayları

### Gaussian Blur Filter
- **Amaç**: Gürültü azaltma ve yumuşatma
- **Parametreler**: sigma değerleri (0.5, 1.0, 1.5, 2.0)
- **Kullanım Alanı**: Gürültülü görüntüler

### Median Filter
- **Amaç**: Tuz-biber gürültüsü temizleme
- **Parametreler**: Çekirdek boyutu (3, 5, 7)
- **Kullanım Alanı**: İmpuls gürültüsü

### Laplacian Enhancement
- **Amaç**: Kenar keskinleştirme
- **Parametreler**: alpha değerleri (0.2, 0.5, 0.8, 1.0)
- **Kullanım Alanı**: Bulanık görüntüler

### Sobel Enhancement
- **Amaç**: Gradyan tabanlı kenar geliştirme
- **Parametreler**: alpha değerleri (0.2, 0.5, 0.8, 1.0)
- **Kullanım Alanı**: Kenar vurgusu

### Histogram Equalization
- **Amaç**: Global kontrast iyileştirme
- **Kullanım Alanı**: Düşük kontrastlı görüntüler

### CLAHE (Adaptive Histogram Equalization)
- **Amaç**: Yerel kontrast geliştirme
- **Parametreler**: clip_limit ve tile_size
- **Kullanım Alanı**: Yerel kontrast problemleri

### Bilateral Filter
- **Amaç**: Kenar koruyucu yumuşatma
- **Parametreler**: sigma_spatial, sigma_intensity
- **Kullanım Alanı**: Gürültü azaltma + kenar koruma

### Gamma Correction
- **Amaç**: Parlaklık ve kontrast ayarı
- **Parametreler**: gamma değerleri (0.5, 0.8, 1.2, 1.5, 2.0)
- **Kullanım Alanı**: Parlaklık düzeltme

### Pansharpening Methods
- **Brovey**: Hızlı ve etkili
- **IHS**: Renk koruyucu
- **PCA**: İstatistiksel yaklaşım

## Önerilen Kullanım Sırası

### Gürültülü Görüntüler için:
1. `median_filter.py` veya `bilateral_filter.py`
2. `adaptive_histogram_equalization.py`
3. `laplacian_enhancement.py`

### Düşük Kontrastlı Görüntüler için:
1. `contrast_stretching.py`
2. `adaptive_histogram_equalization.py`
3. `gamma_log_transforms.py`

### Bulanık Görüntüler için:
1. `highboost_unsharp.py`
2. `laplacian_enhancement.py`
3. `sobel_enhancement.py`

### Çok Spektrallı Veriler için:
1. `pansharpening_methods.py`
2. `contrast_stretching.py`
3. `adaptive_histogram_equalization.py`

## Çıktı Dosyaları

Her filter çalıştırıldığında aşağıdaki formatta dosyalar oluşturur:
- `Image_HW2_[filter_name]_[parameters].tif`

Örnek:
- `Image_HW2_gaussian_blur_sigma1.0.tif`
- `Image_HW2_laplacian_alpha0.5.tif`
- `Image_HW2_histogram_equalized.tif`

## Gereksinimler

```python
numpy
rasterio
scipy
```

Kurulum:
```bash
pip install numpy rasterio scipy
```

## Notlar

- Tüm filtreler `Image_HW2.tif` dosyasını giriş olarak kullanır
- Çıktı dosyaları float32 formatında kaydedilir
- Her filter farklı parametrelerle test edilir
- `run_all_filters.py` tüm filtreleri otomatik çalıştırır ve sonuçları raporlar

## En İyi Sonuçlar İçin

1. Önce `run_all_filters.py` çalıştırarak tüm filtreleri deneyin
2. Görsel olarak en iyi sonuçları karşılaştırın
3. Belirli filterlerle fine-tuning yapın
4. Kombinasyon filtreleri deneyebilirsiniz (örn: önce gürültü azaltma, sonra keskinleştirme)