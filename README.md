<!-- Kalau ada yang mau ditambah/diedit boleh yaa, misal mau tambah emoji, bikin bagus tampilannya, dll. -->
# 🍲 GolekMakanRek! 🍜
**GolekMakanRek!** adalah website untuk Anda para penduduk dan juga turis di Surabaya untuk memilih kuliner sesuai selera.

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
| **Autentikasi & Admin** | Kaindra | **Autentikasi:** Berperan mengatur Registrasi dan Login akun pengguna dan admin. <br> **Admin:** Berperan dalam mengelola konten aplikasi. Admin memiliki hak untuk menambahkan, menghapus, dan mengubah data restoran atau makanan. Selain itu, Admin juga dapat mengawasi dan memoderasi ulasan pengguna. |
| **User Dashboard** | Bram | Berisikan informasi pengguna seperti nama, umur, nomor handphone, dan alamat. Pengguna juga dapat mengedit informasi pribadinya. |
| **Homepage: Search & Filter** | Joshua | Pada homepage, pengguna dapat melihat dan mencari dari data-data yang tersedia pada aplikasi. Pengguna dapat memilih untuk mencari dari daftar restoran ataupun daftar makanan. | 
| **Restaurant Preview** | Ais | Menampilkan restoran-restoran beserta deskripsinya. Ditampilkan pula beserta daftar menu yang tersedia. Daftar menu yang ditampilkan pada fitur ini akan terintegrasi dengan fitur food preview. Rating restoran didapatkan dari akumulasi rating makanan. |
| **Food Preview** | Hafizh | Pada fitur Food Preview, pengguna dapat memberikan ulasan dan rating mengenai produk makanan yang ada pada setiap restoran. Setiap ulasan yang diberikan akan ditampikan ketika pengguna melakukan klik pada button terkait “ulasan produk”. Selain itu, terdapat penghitungan rating yang memungkinkan hasil rata-rata dari setiap rating yang diberikan pengguna akan ditampilkan pada masing-masing produk makanan. |
| **Wishlist** | Falah | Pengguna dapat menambahkan suatu makanan ke dalam daftar berupa wishlist. Daftar ini berisikan makanan-makanan yang diinginkan pengguna. Pengguna dapat melihat daftar tersebut dan mengedit daftarnya seperti menambahkan makanan lainnya dan juga menghapus suatu makanan dari wishlist. |

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
- Menghapus rating makanan
- Menghapus review makanan


## *Dataset* yang Digunakan
Dataset yang digunakan berasal dari [Kaggle - Indonesia food delivery Gofood product list](https://www.kaggle.com/datasets/ariqsyahalam/indonesia-food-delivery-gofood-product-list).

## Deployment URL
Aplikasi kami dapat diakses pada tautan http://joshua-montolalu-golekmakanrek.pbp.cs.ui.ac.id/.
