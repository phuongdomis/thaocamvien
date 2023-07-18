import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import re
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import smtplib
# import pyqrcode as pq
import qrcode
from io import BytesIO





def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background: url(data:image/{"jpg"};base64,{encoded_string.decode()}) no-repeat center fixed;
        -webkit-background-size: cover;
        -moz-background-size: cover;
        -o-background-size: cover;
        background-size: cover;
    }}
    </style>
    """, unsafe_allow_html=True)
add_bg_from_local('images/background2.jpg') 

# Function to resize the image
def resize_image(image_path, width):
    image = Image.open(image_path)
    ratio = width / image.size[0]
    height = int(image.size[1] * ratio)
    resized_image = image.resize((width, height))
    return resized_image

def validate_email(email):
    # Email format regex pattern
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, email):
        return True
    else:
        return False
    

# def create_content_qrcode(content, filename):
#     path = f'images/qrcode/{filename}.png'
#     qr = pq.create(f'{content}')
#     qr.png(path, scale=10, quiet_zone=3)
#     return qr, path


def image_to_base64(image):
    buff = BytesIO()
    image.save(buff, format="JPEG")
    img_str = base64.b64encode(buff.getvalue())
    return img_str


# def image_to_base64(image_path):
#     with open(image_path, "rb") as image_file:
#         encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
#         return encoded_string


def create_content_qrcode(content, ticket_code):
    data = f"{content} - {ticket_code}"
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    encoded_string = image_to_base64(qr_img)
    # qr_img.save(f'images/qrcode/{ticket_code}.png')
    return encoded_string


data_birds = pd.read_csv("data/birds.csv")
data_mammals = pd.read_csv("data/mammals.csv")
data_reptiles = pd.read_csv("data/reptiles.csv")
data_tickets = pd.read_excel("data/tickets.xlsx")

tab1, tab2, tab3, tab4 = st.tabs(["Trang chủ", "Giới thiệu", "Chim và thú", "Mua vé"])
with tab1:
    tab1.write('''
    ### THẢO CẦM VIÊN MỞ CỬA TẤT CẢ CÁC NGÀY TRONG TUẦN 
    #### BAO GỒM LỄ TẾT TỪ 6h ĐẾN 18h   
    ''')
    tab1.image("images/so_do_vuon_thu.jpg")

with tab2:
    tab2.image("images/ZOOBANNER.jpg")
    tab2.write('''
    #### Động vật
    - 7 lớp với hơn 1000 cá thể gồm hàng chục loài có vú, hàng chục giống chim, nhiều giống bò sát và giống có cánh các loại, như: khỉ, gấu ngựa, gấu chó, hổ Đông Dương, hổ Bengal, báo hoa mai, báo lửa, sư tử, tinh tinh, ngựa vằn, linh dương, hươu, nai, heo rừng, mang, nhím, rùa, rái cá, voi châu Á, tê giác trắng, cá sấu hoa cà, cá sấu nước ngọt, trăn đất, công, bò tót,  hà mã, báo đốm Mỹ , hươu cao cổ…   
    ''')
    tab2.write('''
    #### Thực vật
    - Có 1.800 cây gỗ thuộc 260 loài, 23 loài lan nội địa, 33 loài xương rồng, 34 loại bonsai và thảm cỏ xanh trên diện tích 20 ha. Trong đó có những cây cổ thụ hàng trăm năm tuổi, vào hàng quý hiếm nhất Việt nam   
    ''')

with tab3:
    tab5, tab6, tab7, tab8 = st.tabs(["Chim", "Thú", "Bò sát", "Số loài"])
    
    # Display the images
    for index, row in data_birds.iterrows():
        tab5.subheader(row["Name"])
        image_path = "images/" + row["Image"]
        # image = resize_image(image_path, width=400)
        image = Image.open(image_path)
        tab5.image(image, caption=row["Name"], use_column_width=True)
        with tab5.expander("Đọc thêm..."):
            st.write("###### " + row["Introduction"])
            st.write("- Nơi sinh sống: " + str(row["Where_They_Live"]))            
            st.write("- Số loài: " + str(row["Types"]))
    
    for index, row in data_mammals.iterrows():
        tab6.subheader(row["Name"])
        image_path = "images/" + row["Image"]
        # image = resize_image(image_path, width=200)
        image = Image.open(image_path)
        tab6.image(image, caption=row["Name"], use_column_width=True)
        with tab6.expander("Đọc thêm..."):
            st.write("###### " + row["Introduction"])
            st.write("- Nơi sinh sống: " + str(row["Where_They_Live"]))            
            st.write("- Số loài: " + str(row["Types"]))

    for index, row in data_reptiles.iterrows():
        tab7.subheader(row["Name"])
        image_path = "images/" + row["Image"]
        # image = resize_image(image_path, width=200)
        image = Image.open(image_path)
        tab7.image(image, caption=row["Name"], use_column_width=True)
        with tab7.expander("Đọc thêm..."):
            st.write("###### " + row["Introduction"])
            st.write("- Nơi sinh sống: " + str(row["Where_They_Live"]))            
            st.write("- Số loài: " + str(row["Types"]))
    
    tab8.write("#### Chim")   
    bs = data_birds.sort_values(by=["Types"])        
    fig1 = plt.figure()        
    sns.barplot(data=bs, y="Name", x="Types", color='blue')  
    tab8.pyplot(fig1)    

    tab8.write("#### Thú")
    ms = data_mammals.sort_values(by=["Types"], ascending=False)    
    fig2 = plt.figure()        
    sns.barplot(data=ms, y="Name", x="Types")    
    tab8.pyplot(fig2)  

    tab8.write("#### Bò sát")
    rs = data_reptiles.sort_values(by=["Types"], ascending=False)    
    fig3 = plt.figure()
    sns.barplot(data=rs, y="Name", x="Types")    
    tab8.pyplot(fig3) 

with tab4:
    tab4.image("images/ticket.jpg")
    tab4.write('''
    #### Mua Vé Online - Có Vé Tức Thì -  Khỏi Lo Xếp Hàng    
    ''')   
    
    data_tickets['Giá vé (VNĐ)'] = data_tickets['Giá vé'].map(lambda x: f"{x:,.0f}")

    tab4.table(data_tickets[["Loại vé", "Giá vé (VNĐ)"]])
    tab4.write('''
        - (Trẻ em dưới 1m, đi kèm phụ huynh được miễn phí vé vào cổng)
    ''')

# Create a form buy zoo tickets using Python and Streamlit, 
# in this form has 1 textbox to input fullname, 1 textbox to input email, 2 combo boxes to select number of tickets, 
# one submit button, when click this button show selected or input values.
# -> # now, check format of email text_input above

    st.subheader("Mua vé online")
    
    # Input fields
    fullname = st.text_input("Họ tên")
    email_reciever = st.text_input("Email")
    
    # Combo boxes
    num_adult_tickets = st.selectbox(data_tickets.iloc[1,0], range(1, 11), index=0)
    num_child_tickets = st.selectbox(data_tickets.iloc[0,0], range(1, 11), index=0)
    
    # Submit button
    if tab4.button("Mua vé"):
        if validate_email(email_reciever):
            ticket_code = f"YW01{datetime.now().strftime('%Y%m%d%H%M%S')}"
            thanh_tien = num_adult_tickets * data_tickets.iloc[1,1] + num_child_tickets * data_tickets.iloc[0,1]

            # Lưu và csv
            order = {
                'Ho_ten': fullname,
                'Ve_tre_em': num_child_tickets,
                'Ve_nguoi_lon': num_adult_tickets,
                'Tong_cong': thanh_tien,
                'Ma_ve': ticket_code
            }
            tickets = pd.read_csv('data/orders/tickets.csv')
            df = pd.DataFrame([order])
            tickets = pd.concat([tickets, df], ignore_index=True)
            tickets.to_csv('data/orders/tickets.csv', index=False)

            # Gọi hàm để tạo mã QR
            noidung = f'''Họ tên: {fullname}
Số vé người lớn: {str(num_adult_tickets)}
Số vé trẻ em: {str(num_child_tickets)}
Thành tiền: {str('{:,.0f}'.format(thanh_tien))}
'''
            image_string = create_content_qrcode(noidung, ticket_code).decode()

            # Gửi mail
            email_sender = 'ltvpython@csc.hcmus.edu.vn'
            password = 'wvahyrllmszdatpb'
            connection = smtplib.SMTP('smtp.gmail.com', 587)
            connection.starttls()
            connection.login(email_sender, password)
            msg = MIMEMultipart()
            msg['Subject'] = f"{ticket_code} - Xác nhận đặt vé thành công"
            msg['From'] = email_sender
            msg['To'] = email_reciever      
            content = f'''<p>Họ tên: {fullname}</p>
<p>Email: {email_reciever}</p>
<p>Số vé người lớn: {str(num_adult_tickets)}</p>
<p>Số vé trẻ em: {str(num_child_tickets)}</p>
<p>Thành tiền: <b>{str('{:,.0f}'.format(thanh_tien))}</b></p>
<p>Địa chỉ: <a href="https://goo.gl/maps/J64xhAMEKspgdJ5K6" target="_blank">https://goo.gl/maps/J64xhAMEKspgdJ5K6</a></p>
<p><small><a href="https://thaocamvien.streamlit.app/">Thảo Cầm Viên</a></small></p>'''
            mtext = MIMEText(content, "html")
            msg.attach(mtext)
            connection.sendmail(msg["From"], msg["To"], msg.as_string())
            connection.quit()

            # Xuất kết quả
            tab4.success("Đặt mua vé thành công")
            tab4.markdown(content, unsafe_allow_html=True)
            
            # create_content_qrcode(ticket_code, ticket_code)
            # tab4.image(f'images/qrcode/{ticket_code}.png', width= 200)
            tab4.image(f'data:image/{"jpg"};base64,{image_string}', width=200)
        else:
            tab4.error("Vui lòng nhập email chính xác để chúng tôi gửi vé đến quý khách.")
