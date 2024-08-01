import pandas as pd 
import numpy as np 
import pickle as pk 
import streamlit as st
import base64
from PIL import Image, UnidentifiedImageError
import requests
from io import BytesIO

# Load the model
model = pk.load(open('model.pkl', 'rb'))

# Centered header for the app
st.markdown('<h1 class="centered-header">Second Hand Car Price Prediction</h1>', unsafe_allow_html=True)

# Path to your local image file
local_image_path = 'pricewise (1).jpg'

# Function to display image with medium size and centered, with caption
def display_image_centered(image_path, image_id, caption):
    try:
        with open(image_path, 'rb') as f:
            image = Image.open(f)
            # Resize image to medium size
            width, height = image.size
            new_width = 300  # Medium size width
            new_height = int(new_width * height / width)
            image = image.resize((new_width, new_height))
            
            # Encode image to base64
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            # Center the image and add caption using unique id
            st.markdown(
                f"""
                <div id="{image_id}" style="text-align: center;">
                    <style>
                        /* CSS for hovering effect */
                        #{image_id} img {{
                            transition: transform .2s; /* Animation duration */
                        }}
                        #{image_id} img:hover {{
                            transform: scale(1.1); /* Scale up by 10% on hover */
                        }}
                    </style>
                    <img src="data:image/png;base64,{img_str}" alt="Local Image" width="{new_width}">
                    <p>{caption}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # CSS to ensure only this image and caption are centered
            st.markdown(
                f"""
                <style>
                #{image_id} {{
                    text-align: center;
                    display: block;
                    margin-left: auto;
                    margin-right: auto;
                }}
                #{image_id} p {{
                    margin-top: 10px;
                    font-size: 16px;
                    color: #666;
                }}
                
                </style>
                """,
                unsafe_allow_html=True
            )
    except FileNotFoundError:
        st.write("Image file not found. Please check the file path and try again.")

# Usage example
display_image_centered(local_image_path, 'my_image_id', 'Best Cars Only')



# Load the car details CSV
cars_data = pd.read_csv('Cardetailsnew.csv')

# Function to extract the brand name from the car name
def get_brand_name(car_name):
    car_name = car_name.split(' ')[0]
    return car_name.strip()

cars_data['brand_name'] = cars_data['brand_name'].apply(get_brand_name)

# Dictionary to store brand and model image URLs
brand_image_urls = {
    # Add all brand and model image URLs here as before
    # Example:
    'Maruti': {
        'Swift': 'https://imgd.aeplcdn.com/664x374/n/cw/ec/159231/swift-right-front-three-quarter.jpeg?isig=0&q=80',
        'Alto': 'https://imgd.aeplcdn.com/664x374/n/cw/ec/39013/alto-exterior-left-front-three-quarter.jpeg?isig=0&q=80',
        'Baleno': 'https://imgd.aeplcdn.com/664x374/n/cw/ec/102663/baleno-exterior-right-front-three-quarter-66.jpeg?isig=0&q=80'
    },
    'Skoda': {
        'Octavia': 'https://imgd.aeplcdn.com/664x374/n/cw/ec/40371/octavia-exterior-right-rear-three-quarter.jpeg?isig=0&q=80',
        'Rapid': 'https://d2m3nfprmhqjvd.cloudfront.net/blog/20230623154033/spinny-assured-skoda-rapid-jpg.webp',
        'Superb': 'https://imgd.aeplcdn.com/1280x720/n/cw/ec/47692/skoda-superb-exterior0.jpeg'
    },
    'Honda': {
        'Civic': 'https://imgd.aeplcdn.com/664x374/n/cw/ec/27074/civic-exterior-right-front-three-quarter-148155.jpeg?q=80',
        'City': 'https://imgd.aeplcdn.com/1200x900/n/cw/ec/134287/city-exterior-right-front-three-quarter-76.jpeg?isig=0&q=80',
        'Accord': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSIp-n96c-o3ijd67u3x0BdvxCXQW7BIEBB3Q&s'
    },
    'Hyundai': {
        'i20': 'https://imgd.aeplcdn.com/664x374/n/cw/ec/150603/i20-exterior-right-front-three-quarter-7.jpeg?isig=0&q=80',
        'Creta': 'https://images.carandbike.com/car-images/gallery/hyundai/creta/exterior/hyundai-creta.jpg?v=2024-01-17',
        'Elantra': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTgeGGSC2AtMBnt9sUDEPWbXT3wU7nOUzFU3g&s'
    },
    'Toyota': {
        'Camry': 'https://global.toyota/pages/models/images/camry/camry_010_s.jpg',
        'Fortuner': 'https://imgd.aeplcdn.com/664x374/n/cw/ec/44709/fortuner-exterior-right-front-three-quarter-20.jpeg?isig=0&q=80'
    },
    'Ford': {
        'Figo': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRGTV4egHpCrVUFbL_hc47Ccew9BoxoOqbs3g&s',
        'Ecosport': 'https://imgd.aeplcdn.com/1200x900/cw/ec/40369/Ford-EcoSport-Right-Front-Three-Quarter-159249.jpg?wm=0&q=80',
        'Endeavour': 'https://imgd.aeplcdn.com/664x374/n/cw/ec/37640/endeavour-exterior-right-front-three-quarter-149472.jpeg?q=80'
    },
    'Renault': {
        'Duster': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQyUakpwndTVPnKrnMWRd258CTRsBDHN1OTPQ&s',
        'KWID': 'https://imgd.aeplcdn.com/1280x720/n/cw/ec/141125/kwid-exterior-right-front-three-quarter-3.jpeg?isig=0&q=80',
        'Triber': 'https://static.autox.com/uploads/2023/02/Renault-Triber-Electric-Blue-with-Black-Roof.jpg'
    },
    'Mahindra': {
        'XUV500': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR1du11NiAH7ohXIeOy6ndf1eH1FLkxp1ucZA&s',
        'Scorpio': 'https://imgd.aeplcdn.com/664x374/n/cw/ec/128413/scorpio-exterior-right-front-three-quarter-47.jpeg?isig=0&q=80',
        'Thar': 'https://static.autox.com/uploads/2020/10/Mahindra-Thar-Image-1-.jpg'
    },
    'Tata': {
        'Nexon': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ5watdsegaaalHNiZwsc5J2XDS8HThqqRa_Q&s',
        'Harrier': 'https://imgd.aeplcdn.com/664x374/n/cw/ec/139245/harrier-facelift-right-front-three-quarter-4.jpeg?isig=0&q=80',
        'Tiago': 'https://imgd.aeplcdn.com/664x374/n/cw/ec/39345/tiago-exterior-right-front-three-quarter-26.jpeg?isig=0&q=80'
    },
    'Chevrolet': {
        'Beat': 'https://stimg.cardekho.com/images/carexteriorimages/930x620/Chevrolet/Chevrolet-Beat/84/1560334401858/front-left-side-47.jpg',
        'Spark': 'https://stimg.cardekho.com/images/car-images/large/Chevrolet/Chevrolet-Spark/caviar-black.jpg',
        'Cruze': 'https://stimg.cardekho.com/images/car-images/large/Chevrolet/Chevrolet-Cruze/Caviar-Black.jpg?impolicy=resize&imwidth=420'
    },
    'Datsun': {
        'GO': 'https://imgd.aeplcdn.com/1056x594/n/5vajcsa_1461061.jpg?q=80',
        'RediGO': 'https://imgd.aeplcdn.com/664x374/n/cw/ec/45245/datsun-redi-go-right-front-three-quarter19.jpeg?q=80',
    },
    'Jeep': {
        'Compass': 'https://content.carlelo.com/uploads/variant-option/MAsRrpcocZiayRW3e0hJVP60a6QEN84zWga5rFAi.webp',
        'Wrangler': 'https://imgd.aeplcdn.com/664x374/n/cw/ec/174977/wrangler-facelift-right-front-three-quarter.jpeg?isig=0&q=80',
        'Grand': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT-HpioP2GXX7AfE6pB_KFIqbnIVkQatKg1zA&s'
    },
    'Mercedes-Benz': {
        'GLA': 'https://imgd.aeplcdn.com/664x374/n/cw/ec/169161/gla-facelift-right-front-three-quarter-2.jpeg?isig=0&q=80',
        'S-Class': 'https://images.carandbike.com/car-images/colors/mercedes-benz/c-class/mercedes-benz-c-class-obsidian-black.jpg?v=1652343520',
        'E-Class': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTnW0vHv3uIaKTWKiHuKeSH6H52gV7ezMwoTQ&s'
    },
    'Mitsubishi': {
        'Lancer': 'https://images.carandbike.com/car-images/large/mitsubishi/lancer/mitsubishi-lancer.jpg?v=5',
        'Pajero': 'https://imgd.aeplcdn.com/1280x720/ec/b8/0e/9739/img/m/Mitsubishi-Pajero-Sport-Right-Front-Three-Quarter-52939_ol.jpg?t=170422253&t=170422253&q=80',
    },
    'Audi': {
        'A4': 'https://stimg.cardekho.com/images/car-images/930x620/Audi/A4/10548/1689673922795/221_Tango-Red-Metallic_d2525a.jpg?impolicy=resize&imwidth=420',
        'Q7': 'https://stimg.cardekho.com/images/carexteriorimages/930x620/Audi/Q7/10558/1689594791308/front-left-side-47.jpg?impolicy=resize&imwidth=420',
        'Q5': 'https://imgd.aeplcdn.com/664x374/n/cw/ec/53591/q5-exterior-right-front-three-quarter-36.jpeg?isig=0&q=80'
    },
    'Volkswagen': {
        'Polo': 'https://imgd-ct.aeplcdn.com/1056x660/n/cw/ec/94019/left-rear-three-quarter9.jpeg?wm=0&q=80',
        'Vento': 'https://imgd.aeplcdn.com/1280x720/cw/ec/26563/Volkswagen-Vento-Right-Front-Three-Quarter-169094.jpg?wm=0&q=80',
        'Tigor': 'https://cdni.autocarindia.com/ExtraImages/20210323101141_VW_Taigun_t_cross.jpg'
    },
    'BMW': {
        '3': 'https://images.carandbike.com/car-images/colors/bmw/3-series/bmw-3-series-carbon-black.jpg?v=1671446468',
        '5': 'https://static.autox.com/uploads/2021/06/2021-BMW-5-Series-static2.jpg',
        'X5': 'https://stimg.cardekho.com/images/car-images/large/BMW/X5-2023/10452/1688992724639/front-left-side-47.jpg'
    },
    'Nissan': {
        'Micra': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTVdRwTvNoev5Bqq4hs0tcdB2DbR3TzuGASMg&s',
        'Sunny': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSEp7CL4tWKpDJLTuMoKryXk6zam3IU4shMfw&s',
        'Terrano': 'https://imgd.aeplcdn.com/1280x720/cw/ec/28376/Nissan-Terrano-Front-view-93548.jpg?wm=0&q=80'
    },
    'Lexus': {
        'ES': 'https://imgd.aeplcdn.com/664x374/n/q1nkgua_1546607.jpg?q=80',
        'Logan': 'https://imgd.aeplcdn.com/664x374/n/cw/ec/44615/lexus-lc-500h-right-front-three-quarter10.jpeg?q=80',
        'BRV': 'https://imgd.aeplcdn.com/664x374/n/cw/ec/139465/rx-exterior-right-front-three-quarter-6.jpeg?isig=0&q=80',
    },
    'Jaguar': {
        'XF': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTwEeMy1wCD0rmGnLgqOvtW5JReWLfhoq1eKw&s',
        'XE': 'https://stimg.cardekho.com/images/carexteriorimages/930x620/Jaguar/XE/6836/1578638648168/front-left-side-47.jpg?imwidth=890&impolicy=resize',
        'Fusion': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSc0NDT948epym9upK072TTM8AyacK4DTYr2g&s'
    },
    'MG': {
        'Hector': 'https://imgd-ct.aeplcdn.com/664x415/n/cw/ec/130583/hector-exterior-front-view.jpeg?isig=0&q=80',
        'One': 'https://stimg.cardekho.com/images/carexteriorimages/930x620/MG/Gloster/9295/1719724532394/front-left-side-47.jpg?impolicy=resize&imwidth=420'
    },
    'Volvo': {
        'XC40': 'https://stimg.cardekho.com/images/car-images/930x620/Volvo/XC40/9320/1676368678055/221_Fjord-Blue_2c3d4d.jpg?impolicy=resize&imwidth=420',
        'XC60': 'https://imgd.aeplcdn.com/642x336/n/cw/ec/131131/xc60-exterior-right-front-three-quarter-3.jpeg?isig=0&q=80',
        'XC90': 'https://financialexpresswpcontent.s3.amazonaws.com/uploads/2017/01/Volvo-XC90-main-480.jpg'
    },
    'Daewoo': {
        'Matiz': 'https://images.carandbike.com/car-images/big/daewoo/matiz/daewoo-matiz.jpg?v=4',
        'Fluence': 'https://c8.alamy.com/zooms/9/262d46fb76b24883bf51f6e8bb897fbc/b4dkpd.jpg',
    },
    'Kia': {
        'Seltos': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Kia_Seltos_SP2_PE_Snow_White_Pearl_%286%29_%28cropped%29.jpg/640px-Kia_Seltos_SP2_PE_Snow_White_Pearl_%286%29_%28cropped%29.jpg',
        'Sonata': 'https://media.zigcdn.com/media/model/2023/Dec/kia-sonet_600x400.jpg',
    },
    'Fiat': {
        'Punto': 'https://auto.economictimes.indiatimes.com/files/retail_files/punto-evo-1504015893-prod-var.jpg',
        'Fiesta': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSM1eeRpS-dNGuZLTIJt4ZwTCi_u4Qq-eHC3A&s',
        'Linea': 'https://imgd.aeplcdn.com/664x374/cw/ec/12624/Fiat-Linea-Exterior-128099.jpg?wm=0&q=80',
    },
    'Force': {
        'Gurkha': 'https://imgd.aeplcdn.com/664x374/n/cw/ec/124851/gurkha-exterior-right-front-three-quarter-26.jpeg?isig=0&q=80',
        'Trailblazer': 'https://imgd.aeplcdn.com/664x374/n/cw/ec/135589/trax-cruiser-exterior-right-front-three-quarter-2.jpeg?isig=0&q=80',
        'One': 'https://imgd.aeplcdn.com/664x374/ec/8326/img/l/7390.jpg?v=201711021421&q=80'
    },
    'Ambassador': {
        'Classic': 'https://stimg.cardekho.com/car-images/carexteriorimages/large/HindustanMotors/Hindustan-Motors-Ambassador-Avigo-1800-ISZ-MPFI/front-left-side-046.jpg?imwidth=420&impolicy=resize',
        'CR-V': 'https://i.pinimg.com/originals/69/60/5b/69605bfa24c98ef9846d970285cccb86.jpg',
        'Aveo': 'https://i.pinimg.com/736x/d9/a5/ee/d9a5eeeda52b779da8fe7aca43a47973.jpg'
    },
    'Ashok Leyland': {
        'Kicks': 'https://stimg.cardekho.com/images/car-images/large/Ashok-Leyland/Ashok-Leyland-Stile/ashok-leyland-stile-sparkling-white.jpg',
        'Spark': 'https://5.imimg.com/data5/SELLER/Default/2023/3/293817486/AM/LY/MD/95718596/4-tyre-ashok-leyland-partner-mini-truck.jpeg'
    },
    'Isuzu': {
        'D-Max': 'https://stimg.cardekho.com/images/carexteriorimages/930x620/Isuzu/D-Max/9422/1667896979680/front-left-side-47.jpg?impolicy=resize&imwidth=420',
        'MUX': 'https://stimg.cardekho.com/images/carexteriorimages/930x620/Isuzu/MU-X/9889/1681734066714/front-left-side-47.jpg?impolicy=resize&imwidth=420',
        'MU': 'https://www.team-bhp.com/forum/attachments/official-new-car-reviews/1557868d1474609325-isuzu-d-max-v-cross-official-review-2015isuzudmaxdiabloofficialimages1.jpg'
    },
    'Opel': {
        'CrossPolo': 'https://images.carandbike.com/car-images/large/opel/corsa/opel-corsa.jpg?v=5',
        'Astra': 'https://images.91wheels.com/assets/c_images/main/terra/astra/terra-astra-1594366080.jpg',
        'Venture': 'https://stimg.cardekho.com/images/carexteriorimages/930x620/Opel/Opel-Vectra/761/1562830849233/front-left-side-47.jpg'
    }
}

# Select car brand
brand_name = st.selectbox('Select Car Brand', list(brand_image_urls.keys()))

# Select car model based on brand
if brand_name:
    model_name = st.selectbox('Select Car Model', list(brand_image_urls[brand_name].keys()))

    # Fetch car image based on brand and model name
    car_image_url = brand_image_urls[brand_name][model_name]
    response = requests.get(car_image_url)
    try:
        car_image = Image.open(BytesIO(response.content))
        st.image(car_image, caption=f'{brand_name} {model_name} Preview', use_column_width=True)
    except UnidentifiedImageError:
        st.error(f"Could not load image for {brand_name} {model_name}. Please check the URL.")

# Input sliders for car details
year = st.slider('Car Manufactured Year', 1994, 2024)
km_driven = st.slider('No of kms Driven', 11, 200000)
fuel = st.selectbox('Fuel type', cars_data['fuel'].unique())
seller_type = st.selectbox('Seller type', cars_data['seller_type'].unique())
transmission = st.selectbox('Transmission type', cars_data['transmission'].unique())
owner = st.selectbox('Owner type', cars_data['owner'].unique())
mileage = st.slider('Car Mileage', 10, 40)
engine = st.slider('Engine CC', 700, 5000)
max_power = st.slider('Max Power', 0, 200)
seats = st.slider('No of Seats', 5, 10)

# Prediction button
if st.button("Predict"):
    input_data_model = pd.DataFrame(
        [[brand_name, model_name, year, km_driven, fuel, seller_type, transmission, owner, mileage, engine, max_power, seats]],
        columns=['brand_name','model_name', 'year', 'km_driven', 'fuel', 'seller_type', 'transmission', 'owner', 'mileage', 'engine', 'max_power', 'seats']
    )

    # Convert categorical data to numerical
    input_data_model['brand_name'].replace(['Maruti', 'Skoda', 'Honda', 'Hyundai', 'Toyota', 'Ford', 'Renault',
       'Mahindra', 'Tata', 'Chevrolet', 'Datsun', 'Jeep', 'Mercedes-Benz',
       'Mitsubishi', 'Audi', 'Volkswagen', 'BMW', 'Nissan', 'Lexus',
       'Jaguar', 'Land', 'MG', 'Volvo', 'Daewoo', 'Kia', 'Fiat', 'Force',
       'Ambassador', 'Ashok', 'Isuzu', 'Opel'], [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31], inplace=True)
    input_data_model['model_name'].replace(['Swift', 'Rapid', 'City', 'i20', 'Xcent', 'Wagon', '800', 'Etios',
       'Figo', 'Duster', 'Zen', 'KUV', 'Ertiga', 'Alto', 'Verito', 'WR-V',
       'SX4', 'Tigor', 'Baleno', 'Enjoy', 'Omni', 'Vitara', 'Verna', 'GO',
       'Safari', 'Compass', 'Fortuner', 'Innova', 'B', 'Amaze', 'Pajero',
       'Ciaz', 'Jazz', 'A6', 'Corolla', 'New', 'Manza', 'i10', 'Ameo',
       'Vento', 'EcoSport', 'X1', 'Celerio', 'Polo', 'Eeco', 'Scorpio',
       'Freestyle', 'Passat', 'Indica', 'XUV500', 'Indigo', 'Terrano',
       'Creta', 'KWID', 'Santro', 'Q5', 'ES', 'XF', 'Wrangler', 'Rover',
       'S-Class', '5', 'X4', 'Superb', 'E-Class', 'Hector', 'XC40', 'Q7',
       'Elantra', 'XE', 'Nexon', 'CLA', 'Glanza', '3', 'Camry', 'XC90',
       'Ritz', 'Grand', 'Matiz', 'Zest', 'Getz', 'Elite', 'Brio', 'Hexa',
       'Sunny', 'Micra', 'Ssangyong', 'Quanto', 'Accent', 'Ignis',
       'Marazzo', 'Tiago', 'Thar', 'Sumo', 'Bolero', 'GL-Class', 'Beat',
       'A-Star', 'XUV300', 'Nano', 'GTI', 'V40', 'CR-V', 'EON', 'RediGO',
       'Captiva', 'Fiesta', 'Seltos', 'Civic', 'Sail', 'Venture',
       'Classic', 'BR-V', 'Ecosport', 'Aria', 'TUV', 'Bolt', 'Accord',
       'Xylo', 'Grande', 'S-Cross', 'Yaris', 'Tavera', 'Linea',
       'Endeavour', 'Aveo', 'Triber', 'Fusion', 'Octavia', 'A4', 'XL6',
       'Santa', 'Spark', 'Aspire', 'Optra', 'Mobilio', 'BRV', 'X6',
       'Cruze', 'GLA', '6', 'NuvoSport', 'Scala', 'Lodgy', 'Pulse',
       'Supro', 'Sonata', 'Renault', 'Kicks', 'Jetta', 'M-Class', 'Teana',
       'Yeti', 'Q3', 'Gurkha', 'Logan', 'A3', 'Dzire', 'Ikon', 'Fluence',
       'Xenon', 'One', '7', 'S60', 'Lancer', 'X7', 'Fabia', 'Platinum',
       'Captur', 'Gypsy', 'Koleos', 'CLASSIC', 'Harrier', 'Punto',
       'Avventura', 'Laura', 'Leyland', 'MUX', 'Astra', 'Tucson',
       'Esteem', 'Winger', 'Qualis', 'Spacio', 'Venue', 'CrossPolo',
       'Kodiaq', 'D-Max', 'X3', 'Land', 'X5', 'Trailblazer', 'MU', 'GLC',
       'XC60', 'S90', 'S-Presso'],
                                      [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197], inplace=True)
    input_data_model['owner'].replace(['First Owner', 'Second Owner', 'Third Owner', 'Fourth & Above Owner', 'Test Drive Car'],
                                      [1, 2, 3, 4, 5], inplace=True)
    input_data_model['fuel'].replace(['Diesel', 'Petrol', 'LPG', 'CNG'], [1, 2, 3, 4], inplace=True)
    input_data_model['seller_type'].replace(['Individual', 'Dealer', 'Trustmark Dealer'], [1, 2, 3], inplace=True)
    input_data_model['transmission'].replace(['Manual', 'Automatic'], [1, 2], inplace=True)

    # Predict the price using the model
    car_price = model.predict(input_data_model)
    st.balloons()

    # Display the predicted price
    st.markdown('Car Price is going to be ₹' + str(car_price[0]))

    # Thank you message
    st.markdown('<h1 class="centered-header">Thank you</h1>', unsafe_allow_html=True)