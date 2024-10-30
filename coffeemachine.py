import streamlit as st

#Statikmetod
#Statik Metotlar, kendisini hangi sınıf veya örneğin çağırdığını bilmez.
# Sadece kendine verilen argümanları bilir, örnek veya sınıf metotları gibi, gizli bir ilk argüman almazlar.
# Bu yönden bakıldığında, bu fonksiyonun sınıf içinde yazılmasıyla, sınıf dışında yazılması arasında, hiçbir fark yoktur.
# Ancak, aynı modül içerisindeki birçok fonksiyonu anlamsal bütünler içinde toplamak gerektiğinde kullanılabilir.
# Bunları tanımlamak için, metot tanımından önce @staticmethod dekoratörü kullanılır.

#st.session_state, her kullanıcı oturumu için yeniden çalıştırmalar arasında değişkenleri paylaşmanın bir yoludur.
# Streamlit, durumu saklama ve sürdürme yeteneğine ek olarak, Geri Aramaları kullanarak durumu değiştirme yeteneğini de ortaya çıkarır.
# Oturum durumu, çok sayfalı bir uygulamanın içindeki uygulamalar arasında da devam eder.


# Başlangıç kaynakları
if 'resources' not in st.session_state:
    st.session_state.resources = {
        'water': 500,
        'milk': 500,
        'coffee': 200,
        'money': 0
    }

# İçecek bilgileri
MENU = {
    'espresso': {'ingredients': {'water': 50, 'coffee': 18}, 'cost': 1.5},
    'latte': {'ingredients': {'water': 200, 'milk': 150, 'coffee': 24}, 'cost': 2.5},
    'cappuccino': {'ingredients': {'water': 250, 'milk': 100, 'coffee': 24}, 'cost': 3.0},
}

class CoffeeMachine:
    # Raporu görüntüler
    @staticmethod
    def report():
        st.write("### Current Resources:")
        for item, amount in st.session_state.resources.items():
            if item == 'money':
                st.write(f"{item.capitalize()}: ${amount:.2f}")
            else:
                st.write(f"{item.capitalize()}: {amount}ml")

    # Kaynakları kontrol eder
    @staticmethod
    def check_resources(drink):
        for item, amount in MENU[drink]['ingredients'].items():
            if st.session_state.resources[item] < amount:
                st.write(f"Sorry, there is not enough {item}.")
                return False
        return True

    # Ödeme işlemi
    @staticmethod
    def process_payment(cost):
        st.write("Please insert coins.")
        quarters = st.number_input("How many quarters?", min_value=0, step=1) * 0.25
        dimes = st.number_input("How many dimes?", min_value=0, step=1) * 0.10
        nickels = st.number_input("How many nickels?", min_value=0, step=1) * 0.05
        pennies = st.number_input("How many pennies?", min_value=0, step=1) * 0.01
        total = quarters + dimes + nickels + pennies
        if total < cost:
            st.write("Sorry, that's not enough money. Money refunded.")
            return False
        else:
            change = round(total - cost, 2)
            st.write(f"Here is ${change} in change.")
            st.session_state.resources['money'] += cost  # Makineye eklenen para güncelleniyor
            return True

    # Kahve hazırlama ve kaynakları güncelleme
    @staticmethod
    def make_coffee(drink):
        for item, amount in MENU[drink]['ingredients'].items():
            st.session_state.resources[item] -= amount
        st.write(f"Here is your {drink}. Enjoy!")
        CoffeeMachine.report()  # Sipariş sonrası güncellenmiş raporu göster

# Streamlit arayüzü
st.title("Coffee Machine")

# Kullanıcı kahve seçimi
choice = st.selectbox("What would you like?", ("espresso", "latte", "cappuccino", "report", "off"))

# Seçim işlemleri
if choice == "report":
    CoffeeMachine.report()
elif choice == "off":
    st.write("Turning off the coffee machine.")
else:
    if CoffeeMachine.check_resources(choice):
        if CoffeeMachine.process_payment(MENU[choice]['cost']):
            CoffeeMachine.make_coffee(choice)
