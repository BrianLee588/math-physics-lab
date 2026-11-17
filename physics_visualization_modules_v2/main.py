from visualizations import run_newton, run_incline

def main():
    print("高中物理互動視覺化")
    print("1. 牛頓第二運動定律")
    print("2. 摩擦力與斜面")
    choice = input("請選擇模擬主題（1/2）：").strip()
    if choice == "1":
        run_newton()
    elif choice == "2":
        run_incline()
    else:
        print("輸入錯誤，請重新執行。")

if __name__ == "__main__":
    main()
