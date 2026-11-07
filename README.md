# Mobil Robot - ROS 2 ve Gazebo

Bu proje, ROS 2 Lyrical ve Gazebo Jetty kullanılarak hazırlanmış özgün bir
diferansiyel sürüşlü mobil robot simülasyonudur. Robot, engelli bir ortamda
LiDAR verisini kullanarak engellerden kaçınır.

## Derleme

Workspace ana klasöründe aşağıdaki komutları çalıştırın:

```bash
cd /path/to/mobile_robot
source /opt/ros/lyrical/setup.bash
colcon build --symlink-install
source install/setup.bash
```

## Simülasyonu çalıştırma

```bash
source /opt/ros/lyrical/setup.bash
source install/setup.bash
ros2 launch robot_bringup bringup.launch.py
```

Tek launch dosyası Gazebo'yu, robotu, ROS-Gazebo bridge bağlantılarını,
engelden kaçma node'unu ve kayıtlı RViz ayarlarını birlikte başlatır.

## Robotu manuel hareket ettirme

İleri hareket:

```bash
ros2 topic pub --rate 10 /cmd_vel geometry_msgs/msg/Twist \\
  "{linear: {x: 0.3}, angular: {z: 0.0}}"
```

Robotu durdurma:

```bash
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \\
  "{linear: {x: 0.0}, angular: {z: 0.0}}"
```

## ROS topic'leri

| Topic | Mesaj tipi | Yön | Açıklama |
|---|---|---|---|
| `/cmd_vel` | `geometry_msgs/msg/Twist` | ROS -> Gazebo | Hareket komutu |
| `/odom` | `nav_msgs/msg/Odometry` | Gazebo -> ROS | Tekerlek odometrisi |
| `/tf` | `tf2_msgs/msg/TFMessage` | Gazebo -> ROS | Koordinat dönüşümleri |
| `/scan` | `sensor_msgs/msg/LaserScan` | Gazebo -> ROS | LiDAR mesafe verileri |
| `/camera/image_raw` | `sensor_msgs/msg/Image` | Gazebo -> ROS | Ön kamera görüntüsü |
| `/camera/camera_info` | `sensor_msgs/msg/CameraInfo` | Gazebo -> ROS | Kamera kalibrasyon bilgisi |
| `/imu` | `sensor_msgs/msg/Imu` | Gazebo -> ROS | IMU yönelim, açısal hız ve ivme verisi |

Aktif topic'leri kontrol etmek için:

```bash
ros2 topic list
ros2 topic echo /scan
ros2 topic echo /camera/image_raw
ros2 topic echo /odom
ros2 topic echo /imu
```

## Engelden kaçma davranışı

`robot_behavior/avoid_obstacles.py` node'u `/scan` topic'ine abone olur ve
`/cmd_vel` üzerinden hareket komutu yayınlar.

- En yakın geçerli LiDAR mesafesi `0.60 m` değerinden küçükse robot döner.
- Engel yoksa robot `0.25 m/s` hızla ileri hareket eder.

## ROS-Gazebo entegrasyonu

`ros_gz_bridge`, ROS topic'leri ile Gazebo Transport topic'leri arasındaki
mesaj dönüşümünü sağlar. Mevcut bridge bağlantıları şunlardır:

```text
/cmd_vel
/odom
/tf
/clock
/scan
/camera/image_raw
/camera/camera_info
/imu
```

## Paketler

- `robot_description`: URDF/Xacro robot modeli.
- `robot_gazebo`: Gazebo dünyası, simülasyon launch dosyası ve bridge'ler.
- `robot_behavior`: Sensör tabanlı engelden kaçma node'u.
- `robot_bringup`: Tüm sistemi başlatan birleşik launch dosyası.

## Mevcut durum

- Özgün URDF/Xacro robot modeli: tamamlandı
- Diferansiyel sürüş Gazebo plugin'i: tamamlandı
- ROS-Gazebo bridge: tamamlandı
- LiDAR ve ön kamera: entegre edildi
- LiDAR tabanlı engelden kaçma: entegre edildi
- RViz otomatik başlatma ve kayıtlı ayarlar: entegre edildi
- IMU sensörü: entegre edildi 
- Temas sensörü: iki kişilik grup için isteğe bağlı
