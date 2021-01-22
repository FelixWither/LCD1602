import RPi.GPIO as GPIO
import time
from PIL import Image

# Define GPIO to LCD mapping
LCD_RS = 24
LCD_E = 23
LCD_D4 = 22
LCD_D5 = 27
LCD_D6 = 18
LCD_D7 = 17

# Define some device constants
LCD_WIDTH = 16  # Maximum characters per line
LCD_CHR = True  # LCD Character mode(Write data to CGRAM/DDRAM)
LCD_CMD = False  # LCD Command mode(Write data to Command RAM)

LCD_LINE_1 = ['10000000', '10000001', '10000010', '10000011', '10000100', '10000101', '10000110', '10000111',
              '10001000', '10001001', '10001010', '10001011', '10001100', '10001101', '10001110', '10001111']
# LCD Display Data RAM(DDRAM) address for each position in the 1st line
LCD_LINE_2 = ['11000000', '11000001', '11000010', '11000011', '11000100', '11000101', '11000110', '11000111',
              '11001000', '11001001', '11001010', '11001011', '11001100', '11001101', '11001110', '11001111']
# LCD Display Data RAM(DDRAM) address for each postion in the 2nd line
CGRAM_C1 = ['01000000', '01000001', '01000010', '01000011', '01000100', '01000101', '01000110', '01000111']
# LCD Character Generator RAM(CGRAM) adress for each line of the first custom character
CGRAM_C2 = ['01001000', '01001001', '01001010', '01001011', '01001100', '01001101', '01001110', '01001111']
# LCD Character Generator RAM(CGRAM) adress for each line of the second custom character
CGRAM_C3 = ['01010000', '01010001', '01010010', '01010011', '01010100', '01010101', '01010110', '01010111']
# LCD Character Generator RAM(CGRAM) adress for each line of the third custom character
CGRAM_C4 = ['01011000', '01011001', '01011010', '01011011', '01011100', '01011101', '01011110', '01011111']
# LCD Character Generator RAM(CGRAM) adress for each line of the fourth custom character
CGRAM_C5 = ['01100000', '01100001', '01100010', '01100011', '01100100', '01100101', '01100110', '01100111']
# LCD Character Generator RAM(CGRAM) adress for each line of the fifth custom character
CGRAM_C6 = ['01101000', '01101001', '01101010', '01101011', '01101100', '01101101', '01101110', '01101111']
# LCD Character Generator RAM(CGRAM) adress for each line of the sixth custom character
CGRAM_C7 = ['01110000', '01110001', '01110010', '01110011', '01110100', '01110101', '01110110', '01110111']
# LCD Character Generator RAM(CGRAM) adress for each line of the seventh custom character
CGRAM_C8 = ['01111000', '01111001', '01111010', '01111011', '01111100', '01111101', '01111110', '01111111']
# LCD Character Generator RAM(CGRAM) adress for each line of the eighth custom character


DEFINED_CHR = ['00000000', '00000001', '00000010', '00000011', '00000100', '00000101', '00000110', '00000111']
# Character Code for 1st-8th Custom Characters

# Timing constants, modify as needed.
E_PULSE = 0.000005
E_DELAY = 0.0005

# Set LCD1602 Connect Ports
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  # Use BCM/BOARD GPIO numbers
GPIO.setup(LCD_E, GPIO.OUT)  # E
GPIO.setup(LCD_RS, GPIO.OUT)  # RS
GPIO.setup(LCD_D4, GPIO.OUT)  # DB4
GPIO.setup(LCD_D5, GPIO.OUT)  # DB5
GPIO.setup(LCD_D6, GPIO.OUT)  # DB6
GPIO.setup(LCD_D7, GPIO.OUT)  # DB7

# Some LCD1602 Commands
Set_4bit_mode = '00110011'  # D7 D6 D5 D4 D3 D2 D1 D0
Initialize = '00110010'
Open_Display = '00001111'
Set_Curser = '00001100'  # Last 2 Digit Sets the Curser On/Off & Blink On/Off
Clear = '00000001'
Curser_Return = '00000010'
Display_mode = '00000110'  #


# Initialize LCD1602
def lcd_init():
    send_data(Set_4bit_mode, LCD_CMD)
    send_data(Initialize, LCD_CMD)
    send_data(Open_Display, LCD_CMD)
    send_data(Display_mode, LCD_CMD)
    send_data(Clear, LCD_CMD)
    time.sleep(E_DELAY)


# If running LCD1602 at 4-bit mode, you should send data 4 bits by 4 bits.
# Known as High bit and Low bit, which can be transfered by this functoin.
def lcd_HLbit(Data, HL):  # HL=true to output high bit, vice versa
    HLbitO = ''
    if HL:
        index = 0
        while index < 4:
            HLbitO += Data[index]
            index += 1
    else:
        index = 4
        while index < 8:
            HLbitO += Data[index]
            index += 1
    return HLbitO


# Send data to LCD1602, using 4-bit mode.
def send_data(Data, mode):
    GPIO.output(LCD_RS, mode)

    HL = True
    HLbitO = lcd_HLbit(Data, HL)
    reset_data_pin()

    GPIO.output(LCD_D7, int(HLbitO[0]))
    GPIO.output(LCD_D6, int(HLbitO[1]))
    GPIO.output(LCD_D5, int(HLbitO[2]))
    GPIO.output(LCD_D4, int(HLbitO[3]))
    lcd_toggle_enable()
    reset_data_pin()

    HL = False
    HLbitO = lcd_HLbit(Data, HL)
    reset_data_pin()

    GPIO.output(LCD_D7, int(HLbitO[0]))
    GPIO.output(LCD_D6, int(HLbitO[1]))
    GPIO.output(LCD_D5, int(HLbitO[2]))
    GPIO.output(LCD_D4, int(HLbitO[3]))
    lcd_toggle_enable()
    reset_data_pin()


# Set all data pins to 0.
def reset_data_pin():
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)


# Send 1 to 'Enable' port to execute oprations.
def lcd_toggle_enable():
    # Toggle enable
    time.sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)
    time.sleep(E_DELAY)


# Display string on LCD1602
def lcd_string(message, line):
    # Send string to display

    message = message.ljust(LCD_WIDTH, " ")

    send_data(line, LCD_CMD)

    for i in range(LCD_WIDTH):
        if len('0' + str(bin(ord(message[i]))[2:])) == 8:
            send_data('0' + str(bin(ord(message[i]))[2:]), LCD_CHR)
        else:
            send_data('0' * (8 - len(str(bin(ord(message[i])))[2:])) + str(bin(ord(message[i]))[2:]), LCD_CHR)


# Clean all the character on screen.
# After this opreation, LCD1602 must wait for a while for a new opreation.
# Otherwise, something unexpected will happen.
def lcd_clean():
    send_data(Clear, LCD_CMD)
    send_data(Curser_Return, LCD_CMD)


# Define a custom character.
# 'Character' variable must be a  'List' that contains every row of the character.
# Refrence to website if you cannot comprehend.
def define_character(CGRAM_Pos, Character):
    index = 0
    for i in CGRAM_Pos:
        send_data(i, LCD_CMD)
        send_data(Character[index], LCD_CHR)
        index += 1


# Display a custom character at a certain place of the screen.
def display_custom_character(LineandPos, CharacterAdress):
    send_data(LineandPos, LCD_CMD)
    send_data(CharacterAdress, LCD_CHR)


# Return Curser to the 1st character place in line 1
def curser_return():
    send_data(Curser_Return, LCD_CMD)


def display_image(ImageAddress, Init_Pos):  # Init_Pos参数必须为整数，代表在从左往右数的第几列开始显示图片
    Img = Image.open(ImageAddress)  # 打开一张图片
    Width = Img.size[0]  # 读取图片宽
    Height = Img.size[1]  # 读取图片高
    Binary_Image = ''  # 定义容器，用于存储图片的二进制形式
    X_index = 0  # 定义索引
    for i in range(Height):  # 逐行逐像素读取图片颜色信息
        for n in range(Width):
            Color = Img.getpixel((n, i))
            Color_Data_Sum = Color[0] + Color[1] + Color[2]
            if Color_Data_Sum <= 100:  # 如果颜色数值的和不大于某个值，按需修改
                Binary_Image = Binary_Image + '0'  # 就写0
                X_index += 1
                if X_index == Width:  # 如果一行数字到了二进制图片边缘
                    Binary_Image = Binary_Image + '\n'  # 换行
                    X_index = 0  # 索引重置
                else:
                    pass
            else:
                X_index += 1
                Binary_Image = Binary_Image + '1'  # 如果图片的数值的和大于某个值，写1
                if X_index == Width:
                    Binary_Image = Binary_Image + '\n'  # 如果一行数字到了二进制图片边缘
                    X_index = 0  # 索引重置
                else:
                    pass

    Binary_Image = Binary_Image.split()  # 分割数据，做成数组，方便后续处理
    Binary_Image.pop(7)  # 弹出LCD1602上不会显示的那两行
    Binary_Image.pop(14)
    X_index = 0  # 定义索引
    Y_index = 0
    CHRC1R1 = []  # 定义容器，装载即将要被写入CGRAM的字符
    CHRC1R2 = []
    CHRC2R1 = []
    CHRC2R2 = []
    CHRC3R1 = []
    CHRC3R2 = []
    Temp_Str = ''  # 定义容器，临时装载字符每一行的数据

    for y in Binary_Image:  # 第一遍遍历，获得第一列第一行和第二行的字符
        if len(CHRC1R1) < 7:
            while X_index < 5 and Y_index < 7:
                Temp_Str += y[X_index]
                X_index += 1
            if X_index == 5:
                CHRC1R1.append(Temp_Str)
                Temp_Str = ''
                X_index = 0
                Y_index += 1
        elif len(CHRC1R2) < 7:
            X_index = 0
            Y_index = 0
            while X_index < 5 and Y_index < 7:
                Temp_Str += y[X_index]
                X_index += 1
            if X_index == 5:
                CHRC1R2.append(Temp_Str)
                Temp_Str = ''
                X_index = 0
                Y_index += 1

    for y in Binary_Image:  # 第二遍遍历，获得第二列第一行和第二行的字符
        if len(CHRC2R1) < 7:
            X_index = 6
            Y_index = 0
            while X_index < 11 and Y_index < 7:
                Temp_Str += y[X_index]
                X_index += 1
            if X_index == 11:
                CHRC2R1.append(Temp_Str)
                Temp_Str = ''
                X_index = 6
                Y_index += 1
        elif len(CHRC2R2) < 7:
            X_index = 6
            Y_index = 0
            while X_index < 11 and Y_index < 7:
                Temp_Str += y[X_index]
                X_index += 1
            if X_index == 11:
                CHRC2R2.append(Temp_Str)
                Temp_Str = ''
                X_index = 6
                Y_index += 1

    for y in Binary_Image:  # 第三遍遍历，获得第三列第一行和第二行的字符
        if len(CHRC3R1) < 7:
            X_index = 12
            Y_index = 0
            while X_index < 17 and Y_index < 7:
                Temp_Str += y[X_index]
                X_index += 1
            if X_index == 17:
                CHRC3R1.append(Temp_Str)
                Temp_Str = ''
                X_index = 12
                Y_index += 1
        elif len(CHRC3R2) < 7:
            X_index = 12
            Y_index = 0
            while X_index < 17 and Y_index < 7:
                Temp_Str += y[X_index]
                X_index += 1
            if X_index == 17:
                CHRC3R2.append(Temp_Str)
                Temp_Str = ''
                X_index = 12
                Y_index += 1

    # 补齐用于定义字符的数据，每个字符必须是8x8
    X_index = 0
    while X_index < len(CHRC1R1):
        CHRC1R1[X_index] = '0' * (8 - len(CHRC1R1[X_index])) + CHRC1R1[X_index]
        X_index += 1
    CHRC1R1.append('00000000')

    X_index = 0
    while X_index < len(CHRC1R2):
        CHRC1R2[X_index] = '0' * (8 - len(CHRC1R2[X_index])) + CHRC1R2[X_index]
        X_index += 1
    CHRC1R2.append('00000000')

    X_index = 0
    while X_index < len(CHRC2R1):
        CHRC2R1[X_index] = '0' * (8 - len(CHRC2R1[X_index])) + CHRC2R1[X_index]
        X_index += 1
    CHRC2R1.append('00000000')

    X_index = 0
    while X_index < len(CHRC2R2):
        CHRC2R2[X_index] = '0' * (8 - len(CHRC2R2[X_index])) + CHRC2R2[X_index]
        X_index += 1
    CHRC2R2.append('00000000')

    X_index = 0
    while X_index < len(CHRC3R1):
        CHRC3R1[X_index] = '0' * (8 - len(CHRC3R1[X_index])) + CHRC3R1[X_index]
        X_index += 1
    CHRC3R1.append('00000000')

    X_index = 0
    while X_index < len(CHRC3R2):
        CHRC3R2[X_index] = '0' * (8 - len(CHRC3R2[X_index])) + CHRC3R2[X_index]
        X_index += 1
    CHRC3R2.append('00000000')

    Generated_CHR = [CHRC1R1, CHRC1R2, CHRC2R1, CHRC2R2, CHRC3R1, CHRC3R2]
    define_character(CGRAM_C3, Generated_CHR[0])
    define_character(CGRAM_C4, Generated_CHR[1])
    define_character(CGRAM_C5, Generated_CHR[2])
    define_character(CGRAM_C6, Generated_CHR[3])
    define_character(CGRAM_C7, Generated_CHR[4])
    define_character(CGRAM_C8, Generated_CHR[5])
    display_custom_character(LCD_LINE_1[Init_Pos], DEFINED_CHR[2])
    display_custom_character(LCD_LINE_2[Init_Pos], DEFINED_CHR[3])
    display_custom_character(LCD_LINE_1[Init_Pos + 1], DEFINED_CHR[4])
    display_custom_character(LCD_LINE_2[Init_Pos + 1], DEFINED_CHR[5])
    display_custom_character(LCD_LINE_1[Init_Pos + 2], DEFINED_CHR[6])
    display_custom_character(LCD_LINE_2[Init_Pos + 2], DEFINED_CHR[7])


# Initialize LCD1602
lcd_init()

# If this script is running as main program.
# Then run the following test program.
if __name__ == '__main__':
    lcd_string("Hello,world!", LCD_LINE_1[0])
    lcd_string("I am RaspPi!", LCD_LINE_2[0])
    time.sleep(5)

    lcd_string("Driver Test Pass!", LCD_LINE_1[0])
    lcd_string("Enjoy using it!", LCD_LINE_2[0])
    time.sleep(5)

    lcd_string("Author @FelixW", LCD_LINE_1[0])
    lcd_string("QQ:642766671", LCD_LINE_2[0])
    time.sleep(5)

    lcd_string("Inspired by:", LCD_LINE_1[0])
    lcd_string("Matt Hawkins", LCD_LINE_2[0])
    time.sleep(5)

    lcd_string("Import in other", LCD_LINE_1[0])
    lcd_string("Python file&use", LCD_LINE_2[0])
    time.sleep(5)

    GPIO.cleanup()
