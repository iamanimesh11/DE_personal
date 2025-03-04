from datetime import datetime
import time
from plyer import notification

def show_notification():
    """Show a notification for the 20-20-20 rule."""
    notification.notify(
        title="20-20-20 Rule Reminder",
        message="Time to take a break! Look at something 20 feet away for 20 seconds.",
        app_name="20-20-20 Reminder",
        timeout=10  # Notification duration in seconds
    )
def show_notification2():
    """Show a notification for the 20-20-20 rule."""
    notification.notify(
        title="20-20-20 Rule Reminder",
        message="20 secodns over,back to work",
        app_name="20-20-20 Reminder",
        timeout=10  # Notification duration in seconds
    )

def start_timer():
    """Start the 20-minute timer."""
    try:
        while True:
            # Wait for 20 minutes (1200 seconds)
            time.sleep(1200)
            # Show the notification
            show_notification()
            print(f"timer appeared at: "+ datetime.now().strftime("%H:%M:%S")
)
            time.sleep(30)
            show_notification2()

    except KeyboardInterrupt:
        print("\nProgram stopped by user.")

if __name__ == "__main__":
    print("20-20-20 Rule Reminder is running.")
    print("Press Ctrl+C to stop.")
    start_timer()

#
# 💛 Jodi Kripya Dhyan Dein! 💛
#
# Aapka "Shaadi Special Gift Express" apni manzoorashuda gati se vilambit hai! 🚂🎁
# Yeh pyaar, duaon aur thodi si der ka bhaari saman lekar chal raha hai.
# Lekin chinta na karein, yeh jaldi hi aapki sukhad grihasti station par pahunchne ki sambhavana hai!
#
# Kripya intezaar ka signal green rakhein aur muskurate rahein! 😄✨