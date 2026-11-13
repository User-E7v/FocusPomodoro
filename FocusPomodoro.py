import time
import os
import json
import datetime
import threading
import winsound
from collections import deque

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print("=" * 70)
    print("  [*]  P O M O D O R O   T I M E R  [*]")
    print("=" * 70)

def print_separator(char="=", length=70):
    print(char * length)

def get_timer_mode():
    print("\n  SELECT TIMER MODE:")
    print("  " + "-" * 40)
    print("  [1] Classic Pomodoro (25 min work, 5 min break)")
    print("  [2] Long Pomodoro   (50 min work, 10 min break)")
    print("  [3] Custom          (Set your own)")
    print("  [4] Study Mode      (45 min work, 15 min break)")
    print("  [5] Quick Session   (15 min work, 3 min break)")
    print("  [6] Deep Work       (90 min work, 20 min break)")
    print("  [7] Timer Only      (Just set a timer)")
    print("  " + "-" * 40)
    
    while True:
        try:
            choice = int(input("  Enter your choice (1-7): "))
            if choice == 1:
                return 25, 5, "Classic Pomodoro"
            elif choice == 2:
                return 50, 10, "Long Pomodoro"
            elif choice == 3:
                work = int(input("  Enter work minutes: "))
                break_time = int(input("  Enter break minutes: "))
                return work, break_time, "Custom"
            elif choice == 4:
                return 45, 15, "Study Mode"
            elif choice == 5:
                return 15, 3, "Quick Session"
            elif choice == 6:
                return 90, 20, "Deep Work"
            elif choice == 7:
                minutes = int(input("  Enter timer minutes: "))
                return minutes, 0, "Timer Only"
            else:
                print("  Invalid choice. Please enter 1-7.")
        except ValueError:
            print("  Please enter a valid number.")

def get_pomodoro_count():
    while True:
        try:
            count = int(input("  How many pomodoros? (1-10): "))
            if 1 <= count <= 10:
                return count
            print("  Please enter between 1 and 10.")
        except ValueError:
            print("  Please enter a valid number.")

def format_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:02d}"

def draw_progress_bar(progress, width=40):
    filled = int(progress * width)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}]"

def get_time_color(remaining):
    if remaining > 60:
        return "\033[92m"
    elif remaining > 30:
        return "\033[93m"
    elif remaining > 10:
        return "\033[95m"
    else:
        return "\033[91m"

def play_sound():
    try:
        if os.name == 'nt':
            winsound.Beep(1000, 500)
            winsound.Beep(1200, 500)
            winsound.Beep(1500, 500)
        else:
            print("\a")
    except:
        pass

def print_ascii_timer(current_seconds, total_initial_seconds, mode, pomodoro_num, total_pomodoros):
    clear_screen()
    print_header()
    
    if total_initial_seconds > 0:
        progress = 1 - (current_seconds / total_initial_seconds)
    else:
        progress = 0
        
    print(f"\n  [-] POMODORO {pomodoro_num}/{total_pomodoros}")
    print(f"  [=] MODE: {mode}")
    print_separator("-", 70)
    
    remaining = format_time(current_seconds)
    color = get_time_color(current_seconds)
    print(f"\n  [@] TIME REMAINING: {color}{remaining}\033[0m")
    
    print(f"\n  {draw_progress_bar(progress)}")
    
    if current_seconds > 0:
        if current_seconds < 10:
            print("\n  [!] WARNING: TIME IS ALMOST UP!")
        elif current_seconds < 30:
            print("\n  [+] Almost there!")
            
    print_separator("-", 70)
    print("\n  [X] Press Ctrl+C to stop timer\n")

def save_stats(stats):
    filename = "pomodoro_stats.json"
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
    except:
        data = {"sessions": [], "total_pomodoros": 0, "total_time": 0}
        
    data["sessions"].append(stats)
    data["total_pomodoros"] += 1
    data["total_time"] += stats["duration"]
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def view_stats():
    try:
        with open("pomodoro_stats.json", 'r') as f:
            data = json.load(f)
            
        clear_screen()
        print_header()
        print("\n  [%] POMODORO STATISTICS")
        print_separator("-", 70)
        
        total_pomodoros = data["total_pomodoros"]
        total_time = data["total_time"]
        avg_time = total_time / total_pomodoros if total_pomodoros > 0 else 0
        
        print(f"\n  [-] TOTAL POMODOROS: {total_pomodoros}")
        print(f"  [T] TOTAL TIME: {total_time // 60}h {total_time % 60}m")
        print(f"  [^] AVG TIME: {avg_time // 60}m {avg_time % 60}s")
        print_separator("-", 70)
        
        print("\n  [=] RECENT SESSIONS:")
        recent = data["sessions"][-10:]
        for i, session in enumerate(recent, 1):
            status = "[+] COMPLETE" if session["completed"] else "[-] STOPPED"
            print(f"  {i}. {status} | Mode: {session['mode']} | Duration: {session['duration']}s")
            
        print_separator("-", 70)
        input("\n  Press Enter to continue...")
        
    except FileNotFoundError:
        print("\n  No statistics available yet. Complete some pomodoros first!")

def get_motivational_message(pomodoros_completed):
    messages = {
        0: "Start your journey with a single pomodoro!",
        1: "Great start! Keep the momentum!",
        2: "You're building a habit!",
        3: "Amazing! You're making progress!",
        4: "Halfway there? Keep going!",
        5: "You're on fire!",
        6: "Incredible dedication!",
        7: "You're unstoppable!",
        8: "Almost at the finish line!",
        9: "One more to go!",
        10: "FOCUS! You are a pomodoro champion!"
    }
    return messages.get(pomodoros_completed, "Legendary! Keep pushing!")

def run_pomodoro(work_minutes, break_minutes, mode, total_pomodoros, pomodoro_num, is_break=False):
    if is_break:
        total_seconds = break_minutes * 60
        display_mode = f"BREAK - {mode}"
    else:
        total_seconds = work_minutes * 60
        display_mode = f"WORK - {mode}"
        
    initial_seconds = total_seconds
    start_time = time.time()
    
    try:
        while total_seconds > 0:
            print_ascii_timer(total_seconds, initial_seconds, display_mode, pomodoro_num, total_pomodoros)
            time.sleep(1)
            total_seconds -= 1
            
        duration = int(time.time() - start_time)
        play_sound()
        
        clear_screen()
        print_header()
        
        if is_break:
            print(f"\n  [+] BREAK COMPLETE!")
            print(f"  [-] Ready for the next pomodoro!")
        else:
            print(f"\n  [+] POMODORO {pomodoro_num} COMPLETE!")
            print(f"  [%] You completed {pomodoro_num}/{total_pomodoros} pomodoros!")
            
        print(f"  [T] Time: {duration // 60}m {duration % 60}s")
        print(f"  [^] {get_motivational_message(pomodoro_num)}")
        print_separator("=", 70)
        
        return True, duration
        
    except KeyboardInterrupt:
        clear_screen()
        print_header()
        print(f"\n  [-] TIMER STOPPED")
        print(f"  [!] Completed {pomodoro_num-1}/{total_pomodoros} pomodoros")
        return False, int(time.time() - start_time)

def main_menu():
    while True:
        clear_screen()
        print_header()
        print("\n  [#] MAIN MENU")
        print_separator("-", 70)
        print("  [1] Start Pomodoro")
        print("  [2] View Statistics")
        print("  [3] How to Use")
        print("  [4] Settings")
        print("  [5] Exit")
        print_separator("-", 70)
        
        choice = input("\n  Enter your choice (1-5): ")
        
        if choice == '1':
            work_minutes, break_minutes, mode = get_timer_mode()
            total_pomodoros = get_pomodoro_count()
            
            completed_pomodoros = 0
            total_session_time = 0
            
            for i in range(1, total_pomodoros + 1):
                completed, duration = run_pomodoro(work_minutes, break_minutes, mode, total_pomodoros, i, False)
                
                if completed:
                    completed_pomodoros += 1
                    total_session_time += duration
                    
                    stats = {
                        "mode": mode,
                        "duration": duration,
                        "completed": True,
                        "pomodoro_num": i,
                        "timestamp": datetime.datetime.now().isoformat()
                    }
                    save_stats(stats)
                else:
                    stats = {
                        "mode": mode,
                        "duration": duration,
                        "completed": False,
                        "pomodoro_num": i,
                        "timestamp": datetime.datetime.now().isoformat()
                    }
                    save_stats(stats)
                    break
                    
                if i < total_pomodoros and break_minutes > 0:
                    input("\n  Press Enter to start break...")
                    completed_break, break_duration = run_pomodoro(0, break_minutes, mode, total_pomodoros, i, True)
                    
            if completed_pomodoros == total_pomodoros:
                clear_screen()
                print_header()
                print("\n  [*] [*] [*] ALL POMODOROS COMPLETED! [*] [*] [*]")
                print(f"  [-] Total: {total_pomodoros} pomodoros")
                print(f"  [T] Total Time: {total_session_time // 60}m {total_session_time % 60}s")
                print("\n  [^] AMAZING WORK! YOU ARE A PRODUCTIVITY MASTER! [^]")
                print_separator("=", 70)
                for _ in range(3):
                    play_sound()
                    time.sleep(0.5)
                input("\n  Press Enter to continue...")
                
        elif choice == '2':
            view_stats()
            
        elif choice == '3':
            clear_screen()
            print_header()
            print("\n  [?] HOW TO USE POMODORO TIMER")
            print_separator("-", 70)
            print("""
  [-] WHAT IS POMODORO?
  The Pomodoro Technique is a time management
  method developed by Francesco Cirillo.
  
  [*] HOW IT WORKS:
  1. Choose a task to work on
  2. Set timer for 25 minutes (or your choice)
  3. Work on the task until the timer rings
  4. Take a short break (5 minutes)
  5. After 4 pomodoros, take a longer break
  
  [!] BENEFITS:
  * Improved focus and concentration
  * Reduced mental fatigue
  * Better time management
  * Increased productivity
  * Maintains work-life balance
  
  [$] AVAILABLE MODES:
  * Classic: 25/5 minutes
  * Long: 50/10 minutes
  * Study: 45/15 minutes
  * Quick: 15/3 minutes
  * Deep Work: 90/20 minutes
  * Custom: Set your own
  * Timer Only: Just a countdown
            """)
            print_separator("-", 70)
            input("\n  Press Enter to continue...")
            
        elif choice == '4':
            clear_screen()
            print_header()
            print("\n  [*] SETTINGS")
            print_separator("-", 70)
            print("""
  [-] AVAILABLE SETTINGS:
  
  * Multiple timer modes available
  * Customizable work/break times
  * Sound notifications
  * Statistics auto-save
  * Progress tracking
  * Keyboard interrupt support
  
  [!] TIPS FOR BETTER FOCUS:
  * Turn off notifications
  * Work in a quiet environment
  * Take breaks away from screen
  * Stay hydrated
  * Stretch during breaks
            """)
            print_separator("-", 70)
            input("\n  Press Enter to continue...")
            
        elif choice == '5':
            clear_screen()
            print_header()
            print("\n  [+] THANK YOU FOR USING POMODORO TIMER!")
            print("  [-] Stay focused and productive!")
            print_separator("=", 70)
            print("\n  [^] \"The secret of getting ahead is getting started.\"")
            print("\n")
            break
            
        else:
            print("  [!] Invalid choice. Please enter 1-5.")
            time.sleep(1)

def main():
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n  [-] Timer interrupted. Goodbye!")
    except Exception as e:
        print(f"\n  [!] An error occurred: {e}")
        print("  Please restart the application.")

if __name__ == "__main__":
    main()