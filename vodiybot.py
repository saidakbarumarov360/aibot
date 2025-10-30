import json
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types, executor
import os

# =====================
# 🔑 API ma'lumotlari
# =====================
BOT_TOKEN = "7987358783:AAF8C1rQJrvqz1NaFvhKWMfykRg6_kNAdB0"
GEMINI_API_KEY = "AIzaSyB2miiCyviJMYz0wyn_VE_eKeufIYYU5f8"
ADMINS = [5921153725]  # Guruh admin IDsi

# =====================
# ⚙️ JSON fayl bilan ishlash
# =====================
BADWORDS_FILE = "badwords.json"

def load_badwords():
    if os.path.exists(BADWORDS_FILE):
        with open(BADWORDS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_badwords(words):
    with open(BADWORDS_FILE, "w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False, indent=2)

badwords = load_badwords()

# =====================
# 🤖 Tizim sozlamalari
# =====================
genai.configure(api_key=GEMINI_API_KEY)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# =====================
# 🔍 Reklama aniqlash
# =====================
async def is_advertisement(text):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        response = model.generate_content(
            f"""
Matnni tahlil qiling: "{text}"
Agar bu reklama, aksiya, chegirma, kanalga taklif, bot reklama yoki spam bo‘lsa qaysi tilda yozilsa ham — "HA" deb yozing.
Agar oddiy savol yoki suhbat bo‘lsa — "YO‘Q" deb yozing.
"""
        )
        if not hasattr(response, "text") or not response.text:
            return False
        return "HA" in response.text.upper()
    except Exception:
        return False

# =====================
# 💬 Savolga javob berish
# =====================
async def get_answer(text):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        response = model.generate_content(
            f"""
Siz "Vodiy Taraqqiyot" MMT vakilisiz. 
Faqat quyidagi savollarga qisqa, aniq va rasmiy tarzda javob bering. 
Agar savol mavzuga aloqador bo‘lmasa, hech narsa yozmang.

1. Ish vaqti haqida so‘rasa -> "Ish vaqti: Dushanba–Juma, 9:00 dan 18:00 gacha. Tushlik: 12:30–13:30"
2. Manzil haqida so‘rasa -> "Manzil: Qashqadaryo viloyati, Qarshi shahar, Islom Karimov ko‘chasi 289-uy. Mo‘ljal: San’at kolleji yonida."
3. Mashinaga qancha summa berasizlar deb so‘rasa -> "Bozor narxining yarmigacha (50–60% gacha)."
4. Telefon haqida so‘rasa -> "Telefon: +998 55 401 10 10"
5. Ishonchnoma yoki generalniy orqali olsa bo‘ladimi -> "Bo‘ladi, agar ishonchnomada garovga qo‘yish huquqi ko‘rsatilgan bo‘lsa."
6. Ish haqi yoki pensiya evaziga beriladimi -> "Ha, beriladi, agar nomida boshqa faol kredit bo‘lmasa."
7. Kredit garov asosida bo‘lsa -> "Garovdagi mashina bozor narxining 50–60 foizigacha baholanadi."
8. Garovsiz kredit bormi deb so‘rasa -> "Ayrim holatlarda kafillik asosida garovsiz kreditlar beriladi."
9. Kafillar kerakmi deb so‘rasa -> "Garovsiz kredit turlarida  kafil talab qilinadi."
10. Garov mashinasi boshqa odam nomida bo‘lsa -> "mashina faqat kredit oluvchi yoki yaqin qarindoshining nomida bo‘lishi kerak."
11. Kredit olish uchun yosh cheklovi -> "18 yoshdan katta shaxslar kredit olishi mumkin."
12. Kredit uchun propiska kerakmi -> "Ha, doimiy yoki vaqtinchalik ro‘yxatdan o‘tgan manzilingiz bo‘lishi kerak."
13. Kredit olish uchun ish joyi kerakmi -> "Ish joyi bo‘lishi tavsiya etiladi, ammo daromad manbai tasdiqlansa bo‘ladi."
14. Kredit arizasi necha kunda ko‘rib chiqiladi -> "Odatda 1 ish kuni ichida natija chiqadi."
15. Kreditni qayta rasmiylashtirish mumkinmi -> "Ba’zi hollarda, sababga qarab muddat uzaytirilishi mumkin."
16. Mashinani haydab yurish mumkinmi -> "Ha, mashina sizda qoladi, bemalol minib yurish mumkin."
17. Mashina 2000-yilgi bo‘lsa bo‘ladimi -> "Odatda 2000-yildan eski mashinalar garov sifatida olinmaydi."
18. Kreditni boshqasining nomiga to‘lab yuborsam bo‘ladimi -> "Bo‘ladi, agar to‘lovda ism-familiya va shartnoma raqami to‘g‘ri ko‘rsatilgan bo‘lsa."
19. Kreditni qanday to‘layman deb so‘rasa -> "To‘lovlar bank kartasi yoki to‘lov tizimlari orqali amalga oshiriladi."
20. Naqd pulda berasizlarmi -> "Ha, naqd pul ko‘rinishida beriladi."
21. Online ariza topshirish mumkinmi -> "Yo‘q, hozirda online topshirib bo‘lmaydi."
22. Filiallaringiz qayerda deb so‘rasa -> "Farg‘ona, Andijon, Namangan, Qashqadaryo va boshqa viloyatlarda filiallarimiz bor."
23. Kreditni to‘lamasam nima bo‘ladi -> "Shartnomada belgilangan penya qo‘llanadi."
24. Kredit olish uchun boshlang‘ich to‘lov kerakmi -> "Hech qanday boshlang'ich to‘lov yo‘q."
25. Kreditni oilaviy nomda olish mumkinmi -> "Yo‘q, faqat bir shaxs nomiga rasmiylashtiriladi."
27. Karta ochish kerakmi -> "Yo‘q, kredit naqd pul shaklida beriladi."
28. Kredit muddatlari haqida so‘rasa -> "Kreditlar odatda 10 oydan 48 oygacha muddat bilan beriladi."
29. Foiz stavkasi haqida so‘rasa -> "Foiz stavkasi yillik olinadigan kredit turiga bog‘liq."
30. Kreditni muddatidan oldin yopish mumkinmi -> "Ha, istalgan vaqtda to‘liq yopish mumkin, foiz undirilmaydi."
31. Kreditni boshqa odamga o‘tkazish mumkinmi -> "Yo‘q, shartnoma faqat o‘sha mijoz nomida qoladi."
32. Kredit tarixi yomon bo‘lsa berasizlarmi -> "Avvalgi qarz to‘langan bo‘lsa, qayta ko‘rib chiqish mumkin."
33. Kredit olish uchun qanday hujjatlar kerak -> "Pasport, daromad to‘g‘risida ma’lumot va transport vositasi hujjatlari."
34. Mashina oldi-sotdi shartnomasi asosida bo‘lsa bo‘ladimi -> "Ha, lekin yangi egasining nomiga o‘tkazilgan bo‘lishi kerak."
35. Texpassportda qarz yoki jarima bo‘lsa -> "Avval to‘liq to‘lab, so‘ng garovga qo‘yish mumkin."
37. Mashinani garovdan yechish jarayoni -> "Kredit to‘liq yopilgach, taqiqdan chiqarib beriladi."
38. Mashinani boshqa viloyatda baholatsa bo‘ladimi -> "Filialimizga kelsangiz baholab beriladi."
39. Kreditni boshqa viloyatda olish mumkinmi -> "Ha, filial joylashgan hududda ariza topshirish kerak."
40. Kredit to‘lovini kechiktirsam nima bo‘ladi -> "Har bir kechiktirilgan kun uchun 1% miqdorida penya hisoblanadi."
41. Agar kartam muddati o‘tsa -> "Bankka murojaat qilib yangilangan kartani taqdim etasiz."
42. Har oyda to‘lov sanasi o‘zgartiriladimi -> "Yo‘q, shartnomada belgilangan sana doimiy bo‘ladi."
43. To‘lovlarni Payme yoki Click orqali to‘lash mumkinmi -> "Ha, to‘lov tizimlari orqali amalga oshiriladi."
44. Kreditni yopganimdan keyin hujjatlar qachon qaytariladi -> "To‘liq yopilganidan so‘ng 1 ish kuni ichida."
45. Kredit sug‘urtasi bormi -> "Yo‘q, sug'urta va baholash harajati olinmaydi."
46. Vodiy Taraqqiyot davlat tashkilotimi -> "Yo‘q, bu xususiy moliyaviy tashkilot."
48. Tashkilotga shaxsan borish shartmi -> "Ha."
49. Kreditni faqat o‘z viloyatimda olamanmi -> "Yo‘q, istalgan filialda olish mumkin."
50, Agar siz bilmagan savol kelsa-> "To'liq malumot uchun 55 401 1010 raqamiga ish vaqtida telefon qiling"

Savol: {text}
"""
        )
        if not hasattr(response, "text") or not response.text:
            return None
        txt = response.text.strip()
        if len(txt) < 3 or "BILMAYMAN" in txt.upper():
            return None
        return txt
    except Exception:
        return None


# =====================
# 💬 Xabarlarni kuzatish
# =====================
@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_group_message(msg: types.Message):
    try:
        text = msg.text.strip().lower()

        # Faqat guruhdagi xabarlar uchun
        if msg.chat.type not in ("group", "supergroup"):
            return

        # 🔞 Taqiqlangan so‘zlar bor-yo‘qligini tekshirish
        for word in badwords:
            if word.lower() in text:
                try:
                    await msg.delete()
                except:
                    pass
                return

        # Reklama bo‘lsa — o‘chiriladi
        if await is_advertisement(text):
            try:
                await msg.delete()
            except:
                pass
            return

        # Faqat kerakli savollarga javob beriladi
        answer = await get_answer(text)
        if answer:
            await msg.reply(answer, disable_notification=True)
    except Exception as e:
        print(f"⚠️ Xatolik: {e}")


# =====================
# 🔒 Faqat adminlar uchun
# =====================
def is_admin(user_id):
    return user_id in ADMINS


# =====================
# 🏁 /start buyrug‘i
# =====================
@dp.message_handler(commands=["start"])
async def start_cmd(msg: types.Message):
    if msg.chat.type != "private":
        return
    await msg.answer(
        "Assalomu alaykum!\nSiz Vodiy Taraqqiyot AI yordamchisiga ulandingiz.\n"
        "Bu bot guruhda savollarga javob beradi.\n\n"
        "🔑 Faqat adminlar uchun buyruqlar:\n"
        "/addword - yangi taqiqlangan so‘z qo‘shish\n"
        "/delword - so‘zni o‘chirish\n"
        "/listwords - barcha so‘zlarni ko‘rish"
    )


# =====================
# ➕ /addword buyrug‘i
# =====================
@dp.message_handler(commands=["addword"])
async def addword_cmd(msg: types.Message):
    if not is_admin(msg.from_user.id):
        return await msg.reply("❌ Sizda bu buyruqdan foydalanish huquqi yo‘q.")
    parts = msg.text.split(maxsplit=1)
    if len(parts) < 2:
        return await msg.reply("❗ Foydalanish: /addword so‘z")
    word = parts[1].strip().lower()
    if word in badwords:
        return await msg.reply("Bu so‘z allaqachon ro‘yxatda bor.")
    badwords.append(word)
    save_badwords(badwords)
    await msg.reply(f"✅ '{word}' so‘zi taqiqlangan so‘zlar ro‘yxatiga qo‘shildi.")


# =====================
# ❌ /delword buyrug‘i
# =====================
@dp.message_handler(commands=["delword"])
async def delword_cmd(msg: types.Message):
    if not is_admin(msg.from_user.id):
        return await msg.reply("❌ Sizda bu buyruqdan foydalanish huquqi yo‘q.")
    parts = msg.text.split(maxsplit=1)
    if len(parts) < 2:
        return await msg.reply("❗ Foydalanish: /delword so‘z")
    word = parts[1].strip().lower()
    if word not in badwords:
        return await msg.reply("Bu so‘z ro‘yxatda yo‘q.")
    badwords.remove(word)
    save_badwords(badwords)
    await msg.reply(f"🗑 '{word}' so‘zi ro‘yxatdan o‘chirildi.")


# =====================
# 📋 /listwords buyrug‘i
# =====================
@dp.message_handler(commands=["listwords"])
async def listwords_cmd(msg: types.Message):
    if not is_admin(msg.from_user.id):
        return await msg.reply("❌ Sizda bu buyruqdan foydalanish huquqi yo‘q.")
    if not badwords:
        return await msg.reply("📭 Hozircha taqiqlangan so‘zlar yo‘q.")
    await msg.reply("🧾 Taqiqlangan so‘zlar:\n" + "\n".join(f"- {w}" for w in badwords))


# =====================
# ▶️ Ishga tushirish
# =====================
if __name__ == "__main__":
    print("✅ Vodiy Taraqqiyot guruhi uchun AI yordamchi ishga tushdi...")
    executor.start_polling(dp, skip_updates=True)
