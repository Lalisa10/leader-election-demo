# Leader Election
Tài liệu về mẫu thiết kế Leader Election
## Mục lục
1. [Giới Thiệu](#giới-thiệu)
2. [Ưu nhược điểm](#ưu-nhược-điểm)
3. [Một số cách triển khai](#một-số-cách-triển-khai)
4. [Demo](#demo)
5. [Tài liệu tham khảo](#tài-liệu-tham-khảo)

## Giới thiệu
Trong hệ thống phân tán, các node giống hệt nhau khi chạy cùng một tác vụ sẽ có thể gặp các vấn đề như xung đột, tranh chấp tài nguyên, thiếu nhất quán hay thiếu hiệu quả. Do đó ta cần một node leader để điều phối công việc của các node còn lại (follower).


Quá trình bầu chọn ra leader được gọi là Leader Election. Quá trình này sẽ được thực hiện khi khởi chạy mỗi khi node leader hiện tại gặp sự cố, khi đó các node còn lại đều sẵn sàng đứng ra làm leader nhưng đảm bảo chỉ có một node được chọn.
## Ưu nhược điểm
### Ưu điểm
- **Giúp cho hệ thống dễ hiểu hơn**: toàn bộ quá trình quản lý và điều phối trong hệ thống được tập trung tại một điểm;
- **Duy trì tính sẵn sàng và tăng độ bền lỗi**: nếu leader bị lỗi, hệ thống có thể bầu chọn leader mới và tự động phục hồi;
- **Đảm bảo tính đồng nhất**: leader có thể kiểm soát tất cả các thay đổi trạng thái trong hệ thống, giúp đảm bảo tính nhất quán của dữ liệu và trạng thái hệ thống;
- **Cải thiện hiệu suất**: leader có thể lưu trữ một bản cache dữ liệu nhất quán và sử dụng lại mỗi khi cần, giảm thiểu chi phí đọc/ghi từ các nguồn dữ liệu khác.
### Nhược điểm
- **Điểm lỗi duy nhất**: nếu leader gặp sự cố mà hệ thống không phát hiện hoặc không khắc phục kịp thời, toàn bộ hệ thống có thể bị gián đoạn hoặc không khả dụng;
- **Giới hạn khả năng mở rộng**: do mọi yêu cầu và dữ liệu đều phải qua leader nên có thể tạo thành một nút cổ chai khi hệ thống mở rộng;
- **Điểm tin cậy duy nhất**: nếu leader làm việc sai lệch mà không có sự kiểm tra hoặc giám sát, nó có thể gây ra các vấn đề nghiêm trọng cho toàn bộ hệ thống.
## Một số cách triển khai:
Có 3 chiến lược chính để chọn ra leader: *cạnh tranh Mutex*, *cài đặt thuật toán* và *sử dụng dịch vụ của bên thứ 3*. 
### Cạnh tranh mutex:
- Các node sẽ cùng cạnh tranh một mutex phân tán được chia sẻ. Node đầu tiên dành được mutex sẽ được bầu chọn là leader. Tuy nhiên hệ thống cần đảm bảo khi leader gặp sự cố thì mutex sẽ được giải phóng và các node còn lại sẽ tiếp tục cạnh tranh để làm leader mới. Chi tiết có ở phần [demo](#demo).
### Sử dụng thuật toán:
**Thuật toán Raft** được sử dụng phổ biến để cài đặt Leader Election. Các bước bao gồm:
- Bắt đầu mỗi nhiệm kì(term), các node đều là follower;
- Nếu một follower không nghe được từ leader trong một khoảng thời gian (election timeout), nó sẽ trở thành một ứng cử viên;
- Ứng cử viên gửi yêu cầu bình chọn đến các node khác, nếu nhận được bình chọn từ số đông, nó sẽ trở thành leader mới;
- Nếu không có node nào được bình chọn từ số đông, một cuộc bầu chọn mới sẽ diễn ra ở nhiệm kì tiếp theo.

![Raft](https://ewzduhvhjkj.exactdn.com/wp-content/uploads/2024/06/28133534/1.1.jpg)

### Sử dụng dịch vụ của bên thứ 3:
**Apache Zookeeper** là một dịch vụ điều phối và đồng bộ cho hệ thống phân tán. Leader Election cũng là một trong những ứng dụng quan trọng mà Apache Zookeeper có thể cung cấp.
Thuật toán cài đặt Leader Election với Apache Zookeeper:
- Mỗi node tạo ra một Sequential Ephermal Znode;
> Sequential: tên các zNode được gắn số thứ tự một cách tuần tự, VD: /election/leader-00001, /election/leader-00002, /election/leader-00003
> Ephermal: Các Znode này sẽ bị xóa khi node ngừng hoạt động. Như vậy các Znode đóng vai trò như một tham chiếu tình trạng hoạt động của node giúp ta biết được node có hoạt động hay không.
- Ta sẽ duy trì hệ thống sao cho node tạo ra zNode với thứ tự nhỏ nhất sẽ được bầu chọn leader;
- Các node sẽ theo dõi (watch) zNode có thứ tự lớn nhất nhỏ hơn số thứ tự của zNode mà nó tạo ra;
- Khi một zNode bị xóa, node theo dõi nó sẽ nhận được thông báo. Sau đó node này sẽ trở thành leader mới nếu zNode bị xóa là của leader hiện tại, ngược lại sẽ chuyển sang theo dõi zNode có thứ tự nhỏ hơn tiếp theo trong chuỗi.
 
## Demo
Đây là ứng dụng ví dụ cách sử dụng lease của blob Azure Storage để triển khai mutex. Mutex này có thể được sử dụng để bầu ra một leader trong các worker(follower) instances khả dụng. Instance đầu tiên có được lease sẽ được bầu làm leader và vẫn là leader cho đến khi giải phóng lease hoặc không thể gia hạn lease. Các worker instances khác có thể tiếp tục giám sát lease blob trong trường hợp leader không còn khả dụng.

Leader sẽ thực hiện ghi dữ liệu thời tiết từ API của [OpenWeatherMap](https://openweathermap.org/). Worker sẽ thực hiện đọc dữ liệu ấy và in ra màn hình.


![Distributed Mutex](https://learn.microsoft.com/en-us/azure/architecture/patterns/_images/leader-election-diagram.png)

Ứng dụng này bao gồm 2 thành phần chính:
- [Distributed Mutex](src/DistributedMutex/DistributedMutex.py): Giúp tiến trình có thể cạnh tranh mutex và thực hiện hành vi theo đúng vai trò của mình (leader/worker).
- [Đọc/ghi dữ liệu](src/DistributedMutex/MySqlHandler.py)

### Các bước cài đặt và trải nghiệm
#### Bước 1:
Trước tiên, bạn cần có tài khoản Azure Storage. Sau đó dán connection string của Storage Account, tên một blob và container chứa nó vào [constant.py](src/DistributedMutex/constant.py)
#### Bước 2:
Chạy lần lượt các lệnh sau:
```shell
pip install -r requirements.txt
python src/DistributedMutex/test.py
```
#### Bước 3:
Tạo thêm nhiều instance của ứng dụng bằng cách mở nhiều terminal khác và chạy lại lệnh.
```
python src/DistributedMutex/test.py
```
Sau đó bạn sẽ chỉ thấy đúng một tiến trình có thể trở thành leader.
#### Bước 4:
Thử tắt tiến trình leader hiện tại đi, sau một khoảng thời gian một trong các tiến trình còn lại sẽ trở thành leader.

## Tài liệu tham khảo:
1. [Leader Election pattern - Azure](https://learn.microsoft.com/en-us/azure/architecture/patterns/leader-election)
2. [Leader Election in Distributed Systems - AWS](https://aws.amazon.com/builders-library/leader-election-in-distributed-systems/)
3. [Understanding Raft Algorithm: Consensus and Leader Election Explained](https://medium.com/@jitenderkmr/understanding-raft-algorithm-consensus-and-leader-election-explained-faadf28fd047)
4. [Understanding the Raft Consensus Algorithm: A Comprehensive Guide](https://www.mindbowser.com/raft-consensus-algorithm-explained/)
5. [Leader election in a Distributed System Using ZooKeeper](https://www.geeksforgeeks.org/leader-election-in-a-distributed-system-using-zookeeper/)


