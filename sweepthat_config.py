import pygame
import os, re

class Config:
    # Screen dimensions based on the 1.8m x 1.2m ratio shown in image
    WIDTH, HEIGHT = 900, 700  # 3:2 ratio matching the image dimensions

    # Card dimensions
    CARD_WIDTH, CARD_HEIGHT = 85, 95

    # Colors matching the image
    COLORS = {
        "WHITE": (255, 255, 255),  # Card background
        "BLACK": (0, 0, 0),        # Text color
        # "BLUE": (173, 216, 230),   # Board background (light blue)
        "DARK_GREEN": (0, 100, 0), # Card border
        "LIGHT_BROWN": (222, 184, 135) # Outer frame
    }

    # Border
    BORDER_SIZE = 20

    # Font
    FONT_PATH = 'font/Retro Gaming.ttf'

    # IMAGES LIST FOR CARD
    card_image_folder = os.path.join(os.path.dirname(__file__), "card_images")
    card_image_f = [f for f in os.listdir(card_image_folder) if f.lower().endswith(".svg")]
    card_image_files = sorted(card_image_f, key=lambda x: int(re.sub(r'\D', '', x)))


    # SOUND LIST
    sound_folder = os.path.join(os.path.dirname(__file__), "sounds")
    sound_f = [f for f in os.listdir(sound_folder) if f.lower().endswith(".wav")]
    sound_files = sorted(sound_f, key=lambda x: int(re.sub(r'\D', '', x)))
    pygame.mixer.init()
    
    # PRACTICE CARD
    card_prac_folder = os.path.join(os.path.dirname(__file__), "card_images")
    card_prac_f = [f for f in os.listdir(card_prac_folder) if f.lower().endswith(".svg")]
    card_prac_files = sorted(card_prac_f, key=lambda x: int(re.sub(r'\D', '', x)))

    # MORE IMAGE
    # asset_image_folder = os.path.join(os.path.dirname(__file__), "images")
    # asset_image_f = [f for f in os.listdir(asset_image_folder) if f.lower().endswith((".svg", ".png"))]
    # asset_image_files = sorted(asset_image_f, key=lambda x: int(re.sub(r'\D', '', x)))
    
    RAHU = [
            {"surface": pygame.image.load("asset/RAHU/15.png"), "pos": "TOP LEFT"},
            {"surface": pygame.image.load("asset/RAHU/16.png"), "pos": "MIDDLE LEFT"},
            {"surface": pygame.image.load("asset/RAHU/17.png"), "pos": "BOTOM LEFT"},
            {"surface": pygame.image.load("asset/RAHU/18.png"), "pos": "TOP RIGHT"},
            {"surface": pygame.image.load("asset/RAHU/19.png"), "pos": "MIDDLE RIGHT"},
            {"surface": pygame.image.load("asset/RAHU/20.png"), "pos": "BOTOM RIGHT"},

        ]
    
    POSITION = ["Top Left", "Middle Left", "Bottom Left", "Top Right", "Middle Right", "Bottom Right"] 


IMAGE_FILES = Config.card_image_files
SOUND_FILES = Config.sound_files

# CORRECT_IMG = pygame.image.load("images/CORRECT.png")
# INCORRECT_IMG = pygame.image.load("images/INCORRECT.png")
# OPPOCORRECT_IMG = pygame.image.load("images/OPPOCORRECT.png")
# LOSE_IMG = pygame.image.load("images/LOSE.png")
# ONW_IMG = pygame.image.load("images/ONE.png")
# TWO_IMG = pygame.image.load("images/TWO.png")
# THREE_IMG = pygame.image.load("images/THREE.png")
# WIN_IMG = pygame.image.load("images/WIN.png")

THAI_BG = [pygame.image.load("backgrounds/1 BG.png"),
           pygame.image.load("backgrounds/2 BG.png"),
           pygame.image.load("backgrounds/3 BG.png"),
           pygame.image.load("backgrounds/4 BG.png"),
           pygame.image.load("backgrounds/5 BG.png")]
# print(THAI_BG) -> <Surface(900x700x32 SW)>
"""
    CARDS
        -1. พระอภัยมณี
            f :  แล้วสอนว่าอย่่าไว้ใจมนุษย์ มันแสนสุดลึกล้ำเหลือกำหนด
            l :  ถึงเถาวัลย์พันเกี่ยวที่เลี้ยวลด ก็ไม่คดเหมือนหนึ่งในน้ำใจคน
        -2. เพลงยาวถวายโอวาท 
            f : ทั้งการุญสุนทราคาวะ ถวายพระวรองค์จำนงสนอง
            l : ขอพึ่งบุญมุลิกาฝ่าละออง พระหน่อสองสุริย์วงศ์ทรงศักดา
        -3. กาพย์เห่เรือ ตอน เห่ชมเรือกระบวน
            f : ปางเสด็จประเวศด้าว ชลาลัย
            l : ทรงรัตนพิมานชัย กิ่งแก้ว
        -4. นิราศภูเขาทอง
            f : ถึงบางพูดพูดดีเป็นศรีศักดิ์ มีคนรักรสถ้อยอร่อยจิต
            l : แม้พูดชั่วตัวตายทำลายมิตร จะชอบผิดในมนุษย์เพราะพูดจา
        -5. ลิิลิตตะเลงพ่าย
            f : เบื้องนั้นนฤนาถผู้ สยามินทร์ เบี่ยงพระมาลาผิน ห่อนพ้อง
            l : ศัสตราวุธอรินทร์ ฤาถูก เพราะพระหัตถ์หากป้อง ปัดด้วยขอทรง
        -6. นมัสการมาตาปิตุคุณ
            f : ข้าขอนบชนกคุณ ชนนีเป็นเค้ามูล
            l : ผู้กอบนุกูลพูน ผดุงจวบเจริญวัย
        -7. รามเกียรติ์ ตอน นารายณ์ปราบนนทก
            f : มาจะกล่าวบทไป ถึงนนทกน้้าใจกล้าหาญ
            l : ตั้งแต่พระสยมภูวญาณ ประทานให้ล้างเท้าเทวา
        -8. สังข์ทอง
            f : ไม่ว่าลูกน้อยเป็นหอยปู อุ้มชูชิดพิสมัย
            l : พระคุณล้ำลบภพไตร จะออกให้เห็นตัวก็กลัวการ
        -9. อนิรุนทธ์คำฉันท์
            f : เทพารักษ์บังนิทรา อนิรุทธราชา บันทมในราตรีกาล
            l : เทพาอุ้มเอาภูบาล จากรถแก้วกาญจน์ รัศมีพพรายพัฬเหา
        -10. ขุนช้างขุนแผน
            f : นางกอดจูบลูบหลังแล้วสั่งสอน อำนวยพรพลายน้อยละห้อยไห้
            l : พ่อไปดีศรีสวัสดิ์กำจัดภัย จนเติบใหญ่ยิ่งยวดได้บวชเรียน
        -11. โคลงโลกนิติ
            f :  โคควายยังชีพได้ เขาหนัง
            l :  เป็นสิ่งเป็นอันยัง อยู่ไซร้
        -12. อิศรญาณภาษิต
            f : ชายข้าวเปลือกหญิงข้าวสารโบราณว่า น้ำพึ่งเรือเสือพึ่งป่าอัชฌาสัย
            l : เราก็จิตคิดดูเล่าเขาก็ใจ รักกันไว้ดีกว่าชังระวังการ
        -13. สามัคคีเภทคำฉันท์
            f : พึงมารยาทยึด สุประพฤติสงวนพรรค์
            l : รื้อริษยาอัน อุปเฉทไมตรี
        -14.  นิราศนรินทร์
            f : อยุศธยายศล่มแล้ว ลอยสวรรค์ ลงฤา 
            l : สิงหาสน์ปรางค์รัตนบรร- เจิดหล้า
        -15. ลิลิตพระลอ
            f : เสียงฦๅเสียงเล่าอ้าง  อันใด พี่เอย
            l : เสียงย่อมยอยศใคร ทั่วหล้า
        -16. บทพากย์เอราวัณ
            f : อินทรชิตบิดเบือนกายิน เหมือนองค์อมรินทร์ ทรงคชเอราวัณ
            l : ช้างนิรมิตรฤทธิแรงแข็งขัน เผือกผ่องผิวพรรณ สีสังข์สะอาดโอฬาร์
        -17. โคลงภาพพระราชพงศาวดาร โคลงพระสุริโยทัยขาดคอช้าง
            f : บังอรอัคเรศผู้ พิศมัย ท่านนา
            l : นามพระสุริโยทัย ออกอ้าง
        -18. โคลงสุภาษิตนฤทุมนาการ
            f : ทำดีไป่เลือกเว้น ผู้ใด ใดเฮย
            l : แต่ผูกไมตรีไป รอบข้าง
        -19. บทเสภาสามัคคีเสวก ตอน วิศวกรรมา
            f : อันชาติใดไร้ศานติสุขสงบ ต้องมัวรบราญรอนหาผ่อนไม่
            l : ณ ชาตินั้นนรชนไม่สนใจ ในกิจศิลปะวิไลละวาดงาม
        -20. อิเหนา ตอน ศึกกะหมังกุหนิง
            f : นางนวลจับนางนวลนอน เหมือนพี่แนบนวลสมรจินตะหรา
            l : จากพรากจับจากจำนรรจา เหมือนจากนางสการะวาตี
        -21. นิคมพจน์กาพย์ห่อโคลง
            f : กงจักรว่าดอกบัว บอกรับ เร็วแฮ
            l : จักรพัดเศียรร้องอู้ จึ่งรู้ ผิดตน
        -22. บทพากย์เอราวัณ
            f : งาหนึ่งเจ็ดโบกขรณี สระหนึ่งย่อมมี เจ็ดกออุบลบันดาล
            l : กอหนึ่งเจ็ดดอกบัวบาน ดอกหนึ่งเบ่งบาน มีกลีบได้เจ็ดกลีบผกา
        -23. กาพย์เห่ชมเครื่องคาวหวาน
            f : มัสมั่นแกงแก้วตา หอมยี่หร่ารสร้อนแรง
            l : ชายใดได้กลืนแกง แรงอยากให้ใฝ่ฝันหา
        -24. กาพย์เรื่อง พระไชยสุริยา
            f : ข้าเจ้าเอา ก ข   เข้ามาต่อ ก กา มี
            l : แก้ไขในเท่านี้   ดีมิดีอย่าตรีชา
        -25. รามเกียรติ์ ตอน หนุมานเผาลงกา
            f : บัดนั้น คำแหงหนุมานทหารใหญ่
            l : ได้ฟังอสุรีก็ดีใจ แกล้งกล่าวใส่ไคล้ด้วยมารยา
        -26. รามเกียรติ์ ตอน ศึกไมยราพ
            f : ถึงที่ขอบสระก็หยุดอยู่ แลดูไปทั่วทุกสถาน
            l : เห็นวานรเผือกผู้อหังการ ล่วงด่านผ่าทางเข้ามา
        -27. ลิลิตโองการแช่งน้ำ
            f : สี่มือถือสังข์จักรคธาธรณี ภีรุอวตาร
            l : อสูรแลงลาญทัก ททัคนีจรนาย ฯ
        แก้เสียงๆๆๆๆๆ-28. ลิลิตตะเลงพ่าย
            f : พระเดชพระแสดงดล	เผด็จคู่ เข็ญแฮ
            l : ถนัดพระอังสาข้อน  ขาดด้าวโดยขวา ฯ
        -29. มงคลสูตรคำฉันท์
            f : หนึ่งคือบ่คบพาล เพราะจะพาประพฤติผิด
            l : หนึ่งคบกะบัณฑิต เพราะจะพาประสบผล
        -30. นิราศพระบาท
            f : ผนังในกุฎีทั้งสี่ด้าน โอฬาร์ฬารทองทาฝาผนัง
            l : จำเพาะมีสี่ด้านทวารบัง ที่พื้นนั่งดาดด้วยแผ่นเงินงาม
        -31. นิราศเมืองแกลง
            f :  ถึงทุกข์ใครในโลกที่โศกเศร้า ไม่เหมือนเราภุมรินถวิลหา 
            l :  จะพลัดพรากจากกันไม่ทันลา ใช้แต่ตาต่างถ้อยสุนทรวอน
        -32. ลิลิตตะเลงพ่าย
            f : พลอยพล้ำเพลียกถ้าท่าน ในรณ
            l : บัดราชฟาดแสงพล พ่ายฟ้อน
        -33. บทละครนอกเรื่องไชยเชษฐ์
            f : เมื่อวันจะพบพระบิตุเรศ ให้บังเหตุโอรสคิดอดสู
            l : น่าเจ็บใจใครหนอเป็นพ่อกู จึงถามมารดาดูทันใด
        -34. มหาเวสสันดรชาดก กัณฑ์กุมาร
            f : ว่าอุเหม่ อุเหม่ พราหมณ์ผู้นี้นี่อาจองทะนงหนอ มาตีลูกต่อหน้าพ่อไม่เกรงใจ
            l : ธชีเอ่ยกูมาอยู่ป่าเปล่าเมื่อไร ทั้งพระขรรค์ศิลป์ชัยก็ถือมา
        -35. เวสสันดรชาดก กัณฑ์มัทรี
            f : สุดโสตแล้วที่แม่จะซับทราบฟังสำเนียง สุดสุรเสียงที่แม่จะร่ำเรียกพิไรร้อง
            l : สุดฝีเท้าที่แม่จะเยื้องย่องยกย่างลงเหยียบดิน ก็สุดสิ้นสุดปัญญาสุดหาสุดค้นสุดเห็นสุดคิด
        -36. รำพันพิลาป สุนทรภู่
            f : อยู่วัดเทพธิดาด้วยบารมี ได้ผ้าปีปัจจัยไทยทาน
            l : ถึงยามเคราะห์ก็เผอิญให้เหินห่าง ไม่เหมือนอย่างอยู่ที่พระวิหาร
"""