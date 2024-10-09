<!-- Kalau ada yang mau ditambah/diedit boleh yaa, misal mau tambah emoji, bikin bagus tampilannya, dll. -->
# 🍲 GolekMakanRek! 🍜
**GolekMakanRek!** adalah website untuk Anda para penduduk dan juga turis di Surabaya untuk memilih kuliner sesuai selera.

## 📜 Back Story
Surabaya, sebagai salah satu kota besar di Indonesia, memiliki kekayaan kuliner yang sangat beragam, mulai dari jajanan kaki lima hingga restoran mewah. Namun, dengan begitu banyak pilihan, baik penduduk lokal maupun wisatawan sering kali kebingungan menentukan tempat makan yang sesuai dengan selera dan kebutuhan mereka. Dari sinilah ide GolekMakanRek! muncul—sebuah platform yang dirancang untuk membantu masyarakat Surabaya dan para wisatawan menjelajahi serta menemukan kuliner terbaik di kota ini dengan mudah. GolekMakanRek! bertujuan menjadi solusi bagi setiap orang yang ingin menikmati hidangan lezat, tanpa harus repot memilih di tengah keramaian kota.

## 👥 Anggota Kelompok
| Nama | NPM | Akun GitHub | 
| -- | -- | -- |
| Nisrina Annaisha Sarnadi | 2306275960 | [aisss](https://github.com/nsrnannaisha) |
| Kaindra Rizq Sachio | 2306274964 | [kaindraa](https://github.com/kaindraa) |
| Muhammad Afwan Hafizh | 2306208855 | [mir4na](https://github.com/mir4na) |
| Joshua Montolalu | 2306275746 | [HamletJr](https://github.com/HamletJr) |
| Ignasius Bramantya Widiprasetya | 2306245604 | [BramantyaWidiprasetya ](https://github.com/BramantyaWidiprasetya) |
| Muhammad Falah Marzuq | 2306202315 | [falahMarzuq](https://github.com/falahMarzuq)

## 🗒️ Deskripsi Aplikasi
**GolekMakanRek!** adalah sebuah website yang memberikan kemudahan bagi penduduk lokal maupun wisatawan untuk menjelajahi berbagai pilihan kuliner di Surabaya. Dengan desain yang sederhana namun intuitif, platform ini memungkinkan pengguna mencari restoran dan makanan sesuai selera mereka. Melalui fitur pencarian yang dapat difilter berdasarkan jenis makanan, lokasi, atau popularitas, pengguna dapat menemukan rekomendasi kuliner mulai dari makanan kaki lima hingga restoran berbintang dengan cepat dan mudah.

Selain hanya melihat deskripsi restoran dan menu yang tersedia, pengguna juga dapat membaca ulasan dan melihat rating dari pengguna lain. Fitur ini sangat berguna untuk membantu dalam memilih tempat makan terbaik berdasarkan pengalaman orang lain. Uniknya, pengguna juga dapat berkontribusi dengan memberikan rating dan ulasan sendiri setelah mencicipi makanan dari restoran yang mereka kunjungi. Rating ini kemudian akan terakumulasi, memberikan gambaran yang lebih akurat tentang kualitas makanan dan layanan di setiap restoran yang terdaftar di GolekMakanRek!.

Pengalaman pengguna semakin dipersonalisasi dengan adanya fitur wishlist, di mana pengguna dapat menyimpan daftar makanan yang ingin dicoba di kemudian hari. Ini membuat GolekMakanRek! tidak hanya sekadar direktori makanan, tetapi juga tempat bagi komunitas kuliner untuk berbagi pengalaman, memberi rekomendasi, dan membantu orang lain menemukan tempat makan terbaik di Surabaya.
## 📔 Daftar Modul
Berikut adalah daftar modul yang akan di-implementasikan:
 
| Modul | Pengembang | Penjelasan |
| -- | -- | -- |
| **Autentikasi & Admin** | All | **Autentikasi:** Berperan mengatur Registrasi dan Login akun pengguna dan admin. <br> **Admin:** Berperan dalam mengelola konten aplikasi. Admin memiliki hak untuk menambahkan, menghapus, dan mengubah data restoran atau makanan. Selain itu, Admin juga dapat mengawasi dan memoderasi ulasan pengguna. |
| **User Dashboard** | Bram | Berisikan informasi pengguna seperti nama, umur, nomor handphone, dan alamat. Pengguna juga dapat mengedit informasi pribadinya. |
| **Homepage: Search, Filter, Like** | Joshua | Pada homepage, pengguna dapat melihat dan mencari dari data-data yang tersedia pada aplikasi. Pengguna dapat memilih untuk mencari dari daftar restoran ataupun daftar makanan. Selain itu, pengguna dapat melakukan reaction yaitu menyukai makanan yang ditampilkan pada Homepage. Nantinya, angka dari *like* tersebut akan dijumlahkan dari semua user yang menyukai makanan tersebut. |
| **Restaurant Preview & Follow** | Ais | Menampilkan restoran-restoran beserta deskripsinya. Ditampilkan pula beserta daftar menu yang tersedia yang akan terintegrasi dengan fitur food preview. Rating restoran didapatkan dari akumulasi rating makanan. Pengguna dapat mem-_follow_ dan meng-_unfollow_ suatu restoran. Daftar restoran yang telah diikuti akan muncul di homepage. |
| **Food Preview** | Hafizh | Pada fitur Food Preview, pengguna dapat memberikan ulasan dan rating mengenai produk makanan yang ada pada setiap restoran. Setiap ulasan yang diberikan akan ditampikan ketika pengguna melakukan klik pada button terkait “ulasan produk”. Selain itu, terdapat penghitungan rating yang memungkinkan hasil rata-rata dari setiap rating yang diberikan pengguna akan ditampilkan pada masing-masing produk makanan. |
| **Wishlist** | Falah | Pengguna dapat menambahkan suatu makanan ke dalam daftar berupa wishlist. Daftar ini berisikan makanan-makanan yang diinginkan pengguna. Pengguna dapat melihat daftar tersebut dan mengedit daftarnya seperti menambahkan makanan lainnya dan juga menghapus suatu makanan dari wishlist. |
| **Forum Kuliner** | Kaindra | Antar para pengguna dapat melakukan komunikasi dalam bentuk forum yang dibuat. Sebagai contoh, Pengguna A membuka topik pembicaraan di forum. Nantinya, Pengguna B atau Pengguna lainnya dapat ikut mengikuti forum tersebut dengan melakukan reply. |

## 🤺 *Role*/Peran Pengguna
### 1. 👨🏻‍💻 Pengguna
#### a. 🔐 Pengguna (terautentikasi)
Pengguna yang sudah melakukan register dan login dapat:
- Melakukan pencarian dan filtering daftar makanan dan restoran.
- Membuka fitur food preview dan restaurant preview.
- Membuka dan mengubah informasi pengguna pada user dashboard.
- Membuka dan menambahkan wishlist pribadi pengguna.
#### b. 🔒 Pengguna (belum terautentikasi)
Pengguna yang belum melakukan register dan login hanya dapat:
- Membuka homepage.
- Melakukan pencarian dan filtering daftar makanan dan restoran.
- Membuka fitur food preview dan restaurant preview.

### 2. ⌨️🖱️ Admin
Role admin memiliki akses untuk mengelola aplikasi.
- Menghapus rating & ulasan makanan
- Menghapus review makanan
- Menambah restaurant
- Menghaous restaurant
- Menambah makanan
- Menghapus makanan
- Menghapus chat forum


## *Dataset* yang Digunakan
Dataset yang digunakan berasal dari [Kaggle - Indonesia food delivery Gofood product list](https://www.kaggle.com/datasets/ariqsyahalam/indonesia-food-delivery-gofood-product-list).

## Deployment URL
Aplikasi kami dapat diakses pada tautan http://joshua-montolalu-golekmakanrek.pbp.cs.ui.ac.id/.
