import random
from typing import List, Tuple
from datetime import datetime
import time

class TOTOLottery:
    def __init__(self):
        self.number_range = range(1, 50)  # Numbers from 1 to 49
        self.numbers_to_pick = 6
        self.additional_number = True

    def generate_winning_numbers(self) -> Tuple[List[int], int]:
        """Generate winning numbers and additional number for TOTO draw"""
        main_numbers = sorted(random.sample(list(self.number_range), self.numbers_to_pick))
        remaining_numbers = list(set(self.number_range) - set(main_numbers))
        additional = random.choice(remaining_numbers)
        return main_numbers, additional

    def check_prize(self, player_numbers: List[int], winning_numbers: List[int], additional_number: int) -> dict:
        """Check prize category based on matching numbers"""
        matches = len(set(player_numbers) & set(winning_numbers))
        has_additional = additional_number in player_numbers
        matching_numbers = list(set(player_numbers) & set(winning_numbers))
        
        result = {
            "prize": "No prize",
            "matching_numbers": matching_numbers,
            "matches_count": matches,
            "has_additional": has_additional,
            "is_jackpot": matches == 6
        }
        
        if matches == 6:
            result["prize"] = "Group 1 Prize"
        elif matches == 5 and has_additional:
            result["prize"] = "Group 2 Prize"
        elif matches == 5:
            result["prize"] = "Group 3 Prize"
        elif matches == 4 and has_additional:
            result["prize"] = "Group 4 Prize"
        elif matches == 4:
            result["prize"] = "Group 5 Prize"
        elif matches == 3 and has_additional:
            result["prize"] = "Group 6 Prize"
        
        return result

    def get_user_numbers(self) -> List[int]:
        """Get and validate user input numbers"""
        while True:
            print("\nEnter 6 different numbers between 1 and 49, separated by spaces:")
            try:
                numbers = list(map(int, input().strip().split()))
                
                if len(numbers) != 6:
                    print("Error: Please enter exactly 6 numbers.")
                    continue
                    
                if len(set(numbers)) != 6:
                    print("Error: Numbers must be unique.")
                    continue
                    
                if not all(1 <= num <= 49 for num in numbers):
                    print("Error: All numbers must be between 1 and 49.")
                    continue
                
                return sorted(numbers)
                
            except ValueError:
                print("Error: Please enter valid numbers.")

    def play_toto(self, player_numbers: List[int]) -> dict:
        """Simulate one TOTO draw and check results"""
        winning_numbers, additional = self.generate_winning_numbers()
        result = self.check_prize(player_numbers, winning_numbers, additional)
        
        return {
            "draw_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "player_numbers": sorted(player_numbers),
            "winning_numbers": winning_numbers,
            "additional_number": additional,
            "result": result
        }

    def simulate_until_jackpot(self, player_numbers: List[int], max_draws: int = 1000000) -> dict:
        """Simulate TOTO draws until hitting the jackpot or reaching max_draws"""
        draws = 0
        prize_counts = {
            "Group 1 Prize": 0,
            "Group 2 Prize": 0,
            "Group 3 Prize": 0,
            "Group 4 Prize": 0,
            "Group 5 Prize": 0,
            "Group 6 Prize": 0,
            "No prize": 0
        }
        jackpot_achieved = False
        start_time = time.time()
        
        progress_interval = max_draws // 20
        next_progress = progress_interval
        
        print("\nSimulating draws... (This might take a while)")
        print("[" + "-" * 20 + "]", end="\r")
        
        for draws in range(1, max_draws + 1):
            winning_numbers, additional = self.generate_winning_numbers()
            result = self.check_prize(player_numbers, winning_numbers, additional)
            
            # Increment the count for the prize category or handle unknown categories
            prize_key = result["prize"]
            if prize_key in prize_counts:
                prize_counts[prize_key] += 1
            else:
                print(f"Unknown prize category encountered: {prize_key}")
            
            if draws >= next_progress:
                progress = int((draws / max_draws) * 20)
                print("[" + "=" * progress + "-" * (20 - progress) + "]", end="\r")
                next_progress += progress_interval
            
            if result["is_jackpot"]:
                jackpot_achieved = True
                break
        
        return {
            "draws": draws,
            "jackpot_achieved": jackpot_achieved,
            "prize_counts": prize_counts,
            "simulation_time": time.time() - start_time,
            "theoretical_odds": self.calculate_odds(),
            "years_equivalent": self.calculate_years(draws)
        }
    
    def calculate_odds(self) -> int:
        """Calculate theoretical odds of winning Group 1 prize"""
        def combinations(n, r):
            from math import factorial
            return factorial(n) // (factorial(r) * factorial(n - r))
        return combinations(49, 6)
    
    def calculate_years(self, draws: int) -> float:
        """Calculate equivalent years if playing twice a week"""
        draws_per_year = 104  # Twice a week
        return round(draws / draws_per_year, 1)

def display_results(result: dict):
    """Display single draw results in a formatted way"""
    print("\n" + "="*50)
    print(f"Draw Date: {result['draw_date']}")
    print(f"Your Numbers: {result['player_numbers']}")
    print(f"Winning Numbers: {result['winning_numbers']}")
    print(f"Additional Number: {result['additional_number']}")
    print("-"*50)
    print(f"Prize Category: {result['result']['prize']}")
    if result['result']['matching_numbers']:
        print(f"Matching Numbers: {result['result']['matching_numbers']}")
    print(f"Total Matches: {result['result']['matches_count']}")
    if result['result']['has_additional']:
        print("You matched the additional number!")
    print("="*50)

def display_simulation_results(numbers: List[int], stats: dict):
    """Display simulation results in a formatted way"""
    print("\n" + "="*60)
    print("TOTO Simulation Results")
    print("="*60)
    print(f"Numbers played: {numbers}")
    
    if stats["jackpot_achieved"]:
        print(f"\n🎉 JACKPOT achieved after {stats['draws']:,} draws!")
    else:
        print(f"\n❌ No jackpot after {stats['draws']:,} draws")
    
    print(f"\nTime taken: {stats['simulation_time']:.2f} seconds")
    print(f"Equivalent to {stats['years_equivalent']:,} years of playing twice a week")
    
    print("\nPrize Distribution:")
    print("-"*60)
    for prize, count in stats["prize_counts"].items():
        percentage = (count / stats["draws"]) * 100
        print(f"{prize:<15}: {count:>8,} ({percentage:>6.2f}%)")
    
    print("\nTheoretical Odds:")
    print("-"*60)
    print(f"Odds of Group 1 Prize: 1 in {stats['theoretical_odds']:,}")
    print("="*60)

def get_user_choice() -> str:
    """Get and validate user menu choice"""
    while True:
        print("\nWhat would you like to do?")
        print("1. Simulate a single draw")
        print("2. Simulate until jackpot (or max attempts)")
        print("3. Exit program")
        choice = input("Enter your choice (1, 2, or 3): ")
        if choice in ['1', '2', '3']:
            return choice
        print("Invalid choice. Please enter 1, 2, or 3.")

def get_play_again_choice() -> tuple:
    """Get user's choice about playing again and whether to use new numbers"""
    while True:
        play_again = input("\nWould you like to play again? (yes/no): ").lower()
        if play_again in ['no', 'n']:
            return False, False
        elif play_again in ['yes', 'y']:
            while True:
                new_numbers = input("Would you like to enter new numbers? (yes/no): ").lower()
                if new_numbers in ['yes', 'no', 'y', 'n']:
                    return True, new_numbers in ['yes', 'y']
                print("Please enter 'yes' or 'no'")
        print("Please enter 'yes' or 'no'")

def main():
    """Main program loop"""
    print("Welcome to Singapore TOTO Lottery Simulator!")
    print("-------------------------------------------")
    
    toto = TOTOLottery()
    player_numbers = toto.get_user_numbers()

    while True:
        choice = get_user_choice()

        if choice == '1':
            result = toto.play_toto(player_numbers)
            display_results(result)
        
        elif choice == '2':
            max_draws = 1000000  # Default maximum draws
            stats = toto.simulate_until_jackpot(player_numbers, max_draws)
            display_simulation_results(player_numbers, stats)
        
        elif choice == '3':
            print("Thank you for playing! Goodbye!")
            break

        # Ask if the user wants to play again
        play_again, enter_new_numbers = get_play_again_choice()
        if not play_again:
            print("Thank you for playing! Goodbye!")
            break
        if enter_new_numbers:
            player_numbers = toto.get_user_numbers()

if __name__ == "__main__":
    main()
