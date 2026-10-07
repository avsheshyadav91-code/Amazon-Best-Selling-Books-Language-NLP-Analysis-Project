"""
Data generator & loader for Amazon Best Selling Books (2009-2022).
Populates authentic bestselling titles with key metadata for language/NLP analysis.
"""

import csv
import os

DATASET_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "bestsellers.csv")

# Curated list of iconic Amazon Bestsellers with realistic multi-year occurrences
BOOK_CATALOG = [
    # Non-Fiction
    ("The 7 Habits of Highly Effective People: Powerful Lessons in Personal Change", "Stephen R. Covey", 4.7, 4725, 16, "Non Fiction", "English", [2009, 2011, 2012, 2013]),
    ("The Four Agreements: A Practical Guide to Personal Freedom", "Don Miguel Ruiz", 4.7, 23308, 6, "Non Fiction", "English", [2016, 2017, 2018, 2019, 2020]),
    ("Atomic Habits: An Easy & Proven Way to Build Good Habits & Break Bad Ones", "James Clear", 4.9, 112000, 12, "Non Fiction", "English", [2019, 2020, 2021, 2022]),
    ("Becoming", "Michelle Obama", 4.8, 61133, 11, "Non Fiction", "English", [2018, 2019]),
    ("Educated: A Memoir", "Tara Westover", 4.7, 45351, 15, "Non Fiction", "English", [2018, 2019, 2020]),
    ("The Subtle Art of Not Giving a F*ck: A Counterintuitive Approach to Living a Good Life", "Mark Manson", 4.6, 26490, 15, "Non Fiction", "English", [2017, 2018, 2019]),
    ("Thinking, Fast and Slow", "Daniel Kahneman", 4.6, 17800, 14, "Non Fiction", "English", [2011, 2012, 2013]),
    ("Outliers: The Story of Success", "Malcolm Gladwell", 4.6, 10426, 20, "Non Fiction", "English", [2009, 2010]),
    ("Quiet: The Power of Introverts in a World That Can't Stop Talking", "Susan Cain", 4.6, 10000, 16, "Non Fiction", "English", [2012, 2013]),
    ("Sapiens: A Brief History of Humankind", "Yuval Noah Harari", 4.7, 34000, 18, "Non Fiction", "English", [2015, 2016, 2017, 2018]),
    ("The Power of Habit: Why We Do What We Do in Life and Business", "Charles Duhigg", 4.6, 16191, 21, "Non Fiction", "English", [2012]),
    ("StrengthsFinder 2.0", "Gallup", 4.0, 5069, 17, "Non Fiction", "English", [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017]),
    ("The 5 Love Languages: The Secret to Love that Lasts", "Gary Chapman", 4.8, 25554, 8, "Non Fiction", "English", [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]),
    ("How to Win Friends & Influence People", "Dale Carnegie", 4.7, 25001, 11, "Non Fiction", "English", [2014, 2015, 2016, 2017, 2018]),
    ("Untamed", "Glennon Doyle", 4.6, 32000, 17, "Non Fiction", "English", [2020, 2021]),
    ("Can't Hurt Me: Master Your Mind and Defy the Odds", "David Goggins", 4.8, 62000, 18, "Non Fiction", "English", [2019, 2020, 2021]),
    ("The Body Keeps the Score: Brain, Mind, and Body in the Healing of Trauma", "Bessel van der Kolk M.D.", 4.8, 71000, 15, "Non Fiction", "English", [2019, 2020, 2021, 2022]),
    ("Caste: The Origins of Our Discontents", "Isabel Wilkerson", 4.8, 28000, 19, "Non Fiction", "English", [2020, 2021]),
    ("Grit: The Power of Passion and Perseverance", "Angela Duckworth", 4.6, 12500, 16, "Non Fiction", "English", [2016, 2017]),
    ("Dare to Lead: Brave Work. Tough Conversations. Whole Hearts.", "Brené Brown", 4.7, 18900, 18, "Non Fiction", "English", [2018, 2019]),
    ("Hillbilly Elegy: A Memoir of a Family and Culture in Crisis", "J. D. Vance", 4.4, 30000, 14, "Non Fiction", "English", [2016, 2017]),
    ("Unbroken: A World War II Story of Survival, Resilience, and Redemption", "Laura Hillenbrand", 4.8, 29651, 16, "Non Fiction", "English", [2010, 2011, 2012, 2014]),
    ("The Life-Changing Magic of Tidying Up: The Japanese Art of Decluttering and Organizing", "Marie Kondō", 4.5, 22641, 11, "Non Fiction", "English", [2015, 2016, 2017]),
    ("Man's Search for Meaning", "Viktor E. Frankl", 4.7, 20500, 9, "Non Fiction", "English", [2017, 2018, 2019]),
    ("Astrophysics for People in a Hurry", "Neil deGrasse Tyson", 4.7, 9374, 9, "Non Fiction", "English", [2017]),
    ("Principles: Life and Work", "Ray Dalio", 4.6, 9500, 22, "Non Fiction", "English", [2017, 2018]),
    ("Bad Blood: Secrets and Lies in a Silicon Valley Startup", "John Carreyrou", 4.7, 16000, 15, "Non Fiction", "English", [2018]),
    ("Born a Crime: Stories from a South African Childhood", "Trevor Noah", 4.8, 38000, 14, "Non Fiction", "English", [2017, 2018, 2019]),
    ("A Promised Land", "Barack Obama", 4.9, 87000, 24, "Non Fiction", "English", [2020]),
    ("Greenlights", "Matthew McConaughey", 4.7, 45000, 18, "Non Fiction", "English", [2020, 2021]),
    ("Rich Dad Poor Dad: What the Rich Teach Their Kids About Money", "Robert T. Kiyosaki", 4.7, 42000, 7, "Non Fiction", "English", [2018, 2019, 2020, 2021]),
    ("The Psychology of Money: Timeless lessons on wealth, greed, and happiness", "Morgan Housel", 4.7, 54000, 16, "Non Fiction", "English", [2020, 2021, 2022]),
    ("Thinking in Bets: Making Smarter Decisions When You Don't Have All the Facts", "Annie Duke", 4.5, 4100, 15, "Non Fiction", "English", [2018]),
    ("Deep Work: Rules for Focused Success in a Distracted World", "Cal Newport", 4.6, 17200, 16, "Non Fiction", "English", [2016, 2017, 2018]),
    ("Clean Code: A Handbook of Agile Software Craftsmanship", "Robert C. Martin", 4.7, 6300, 42, "Non Fiction", "English", [2015, 2017, 2019]),

    # Fiction
    ("Where the Crawdads Sing", "Delia Owens", 4.8, 87841, 15, "Fiction", "English", [2018, 2019, 2020]),
    ("To Kill a Mockingbird", "Harper Lee", 4.8, 26234, 0, "Fiction", "English", [2013, 2014, 2015, 2016, 2019]),
    ("The Great Gatsby", "F. Scott Fitzgerald", 4.4, 11616, 12, "Fiction", "English", [2012, 2013, 2014]),
    ("The Fault in Our Stars", "John Green", 4.7, 50482, 13, "Fiction", "English", [2012, 2013, 2014]),
    ("Gone Girl", "Gillian Flynn", 4.0, 57271, 9, "Fiction", "English", [2012, 2013, 2014]),
    ("The Girl on the Train", "Paula Hawkins", 4.1, 79446, 18, "Fiction", "English", [2015, 2016]),
    ("The Nightingale", "Kristin Hannah", 4.8, 49288, 11, "Fiction", "English", [2015, 2016]),
    ("All the Light We Cannot See", "Anthony Doerr", 4.6, 36348, 14, "Fiction", "English", [2014, 2015]),
    ("The Alchemist", "Paulo Coelho", 4.7, 35799, 15, "Fiction", "English", [2014, 2015, 2016, 2017, 2018, 2019]),
    ("The Midnight Library: A Novel", "Matt Haig", 4.3, 76000, 13, "Fiction", "English", [2020, 2021, 2022]),
    ("The Silent Patient", "Alex Michaelides", 4.5, 83000, 14, "Fiction", "English", [2019, 2020, 2021]),
    ("It Ends with Us: A Novel", "Colleen Hoover", 4.7, 145000, 10, "Fiction", "English", [2021, 2022]),
    ("Verity", "Colleen Hoover", 4.6, 92000, 11, "Fiction", "English", [2021, 2022]),
    ("The Song of Achilles: A Novel", "Madeline Miller", 4.7, 65000, 13, "Fiction", "English", [2021, 2022]),
    ("The Seven Husbands of Evelyn Hugo: A Novel", "Taylor Jenkins Reid", 4.6, 94000, 12, "Fiction", "English", [2021, 2022]),
    ("Klara and the Sun: A Novel", "Kazuo Ishiguro", 4.3, 28000, 16, "Fiction", "English", [2021]),
    ("The Vanishing Half: A Novel", "Brit Bennett", 4.4, 48000, 15, "Fiction", "English", [2020, 2021]),
    ("Circe", "Madeline Miller", 4.6, 42000, 14, "Fiction", "English", [2018, 2019]),
    ("Little Fires Everywhere", "Celeste Ng", 4.5, 46000, 13, "Fiction", "English", [2017, 2018, 2019]),
    ("The Goldfinch: A Novel (Pulitzer Prize for Fiction)", "Donna Tartt", 3.9, 33844, 20, "Fiction", "English", [2013, 2014]),
    ("The Book Thief", "Markus Zusak", 4.6, 23148, 6, "Fiction", "English", [2013, 2014]),
    ("The Martian", "Andy Weir", 4.7, 39459, 9, "Fiction", "English", [2014, 2015]),
    ("Ready Player One", "Ernest Cline", 4.6, 22536, 12, "Fiction", "English", [2017, 2018]),
    ("Crazy Rich Asians", "Kevin Kwan", 4.3, 15200, 10, "Fiction", "English", [2018]),
    ("A Gentleman in Moscow: A Novel", "Amor Towles", 4.7, 39000, 16, "Fiction", "English", [2017, 2018, 2019]),
    ("The Road", "Cormac McCarthy", 4.4, 14500, 11, "Fiction", "English", [2009, 2010]),
    ("Water for Elephants", "Sara Gruen", 4.5, 12658, 12, "Fiction", "English", [2011]),
    ("The Help", "Kathryn Stockett", 4.8, 13871, 6, "Fiction", "English", [2009, 2010, 2011]),
    ("The Girl with the Dragon Tattoo", "Stieg Larsson", 4.4, 10559, 2, "Fiction", "English", [2009, 2010]),
    ("The Girl Who Played with Fire", "Stieg Larsson", 4.5, 7251, 9, "Fiction", "English", [2010]),
    ("The Girl Who Kicked the Hornet's Nest", "Stieg Larsson", 4.7, 7744, 14, "Fiction", "English", [2010, 2011]),
    ("The Catcher in the Rye", "J.D. Salinger", 4.0, 13204, 12, "Fiction", "English", [2009, 2014]),
    ("1984 (Signet Classics)", "George Orwell", 4.7, 21424, 6, "Fiction", "English", [2017]),
    ("Animal Farm", "George Orwell", 4.6, 15200, 7, "Fiction", "English", [2017, 2018]),
    ("Fahrenheit 451", "Ray Bradbury", 4.6, 19800, 8, "Fiction", "English", [2018, 2019]),

    # Children / Young Adult & Classic Series
    ("The Wonky Donkey", "Craig Smith", 4.8, 30183, 4, "Fiction", "English", [2018, 2019]),
    ("Oh, the Places You'll Go!", "Dr. Seuss", 4.9, 21834, 8, "Fiction", "English", [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]),
    ("The Very Hungry Caterpillar", "Eric Carle", 4.9, 19546, 5, "Fiction", "English", [2013, 2014, 2015, 2016, 2017, 2018, 2019]),
    ("Goodnight Moon", "Margaret Wise Brown", 4.8, 18200, 6, "Fiction", "English", [2015, 2016, 2017, 2018, 2019, 2020]),
    ("Brown Bear, Brown Bear, What Do You See?", "Bill Martin Jr.", 4.9, 14344, 5, "Fiction", "English", [2017, 2019]),
    ("Harry Potter Paperback Box Set (Books 1-7)", "J.K. Rowling", 4.9, 13471, 52, "Fiction", "English", [2016]),
    ("Harry Potter and the Chamber of Secrets: The Illustrated Edition", "J.K. Rowling", 4.9, 18042, 30, "Fiction", "English", [2016]),
    ("Harry Potter and the Sorcerer's Stone: The Illustrated Edition", "J.K. Rowling", 4.9, 10052, 22, "Fiction", "English", [2015]),
    ("Harry Potter and the Goblet of Fire: The Illustrated Edition", "J.K. Rowling", 4.9, 7758, 18, "Fiction", "English", [2019]),
    ("Harry Potter and the Cursed Child, Parts 1 & 2, Special Rehearsal Edition Script", "J.K. Rowling", 4.0, 23973, 12, "Fiction", "English", [2016]),
    ("Dog Man: Brawl of the Wild: From the Creator of Captain Underpants", "Dav Pilkey", 4.9, 7235, 4, "Fiction", "English", [2018, 2019]),
    ("Dog Man: Fetch-22: From the Creator of Captain Underpants", "Dav Pilkey", 4.9, 12619, 8, "Fiction", "English", [2019]),
    ("Dog Man: Lord of the Fleas: From the Creator of Captain Underpants", "Dav Pilkey", 4.9, 5470, 6, "Fiction", "English", [2018]),
    ("Dog Man: For Whom the Ball Rolls: From the Creator of Captain Underpants", "Dav Pilkey", 4.9, 9089, 8, "Fiction", "English", [2019]),
    ("Wonder", "R. J. Palacio", 4.8, 21625, 9, "Fiction", "English", [2013, 2014, 2015, 2016, 2017]),
    ("Diary of a Wimpy Kid: The Meltdown (Book 13)", "Jeff Kinney", 4.8, 5881, 8, "Fiction", "English", [2018]),
    ("Diary of a Wimpy Kid: Wrecking Ball (Book 14)", "Jeff Kinney", 4.9, 9413, 8, "Fiction", "English", [2019]),
    ("Diary of a Wimpy Kid: Old School (Book 10)", "Jeff Kinney", 4.8, 6169, 7, "Fiction", "English", [2015]),
    ("Diary of a Wimpy Kid: Hard Luck, Book 8", "Jeff Kinney", 4.8, 6812, 0, "Fiction", "English", [2013]),
    ("Diary of a Wimpy Kid: The Long Haul", "Jeff Kinney", 4.8, 6540, 9, "Fiction", "English", [2014]),

    # Non-English / Multilingual Editions & Translations in Best Sellers
    ("Cien años de soledad (Edición conmemorativa)", "Gabriel García Márquez", 4.8, 14200, 14, "Fiction", "Spanish", [2015, 2018, 2020]),
    ("El principito (The Little Prince Spanish Edition)", "Antoine de Saint-Exupéry", 4.9, 18500, 9, "Fiction", "Spanish", [2016, 2017, 2019, 2021]),
    ("Los cuatro acuerdos: Una guía práctica para la libertad personal", "Don Miguel Ruiz", 4.8, 16800, 8, "Non Fiction", "Spanish", [2017, 2019, 2021]),
    ("El alquimista (Spanish Edition)", "Paulo Coelho", 4.7, 12400, 12, "Fiction", "Spanish", [2014, 2016, 2018]),
    ("Hábitos atómicos: Cambios pequeños, resultados extraordinarios", "James Clear", 4.9, 22000, 14, "Non Fiction", "Spanish", [2020, 2021, 2022]),
    ("Le Petit Prince", "Antoine de Saint-Exupéry", 4.9, 11300, 10, "Fiction", "French", [2015, 2017, 2019]),
    ("L'Étranger (Folio)", "Albert Camus", 4.7, 7800, 11, "Fiction", "French", [2016, 2018]),
    ("Der Vorleser", "Bernhard Schlink", 4.5, 4900, 12, "Fiction", "German", [2012, 2015]),
    ("Die Verwandlung", "Franz Kafka", 4.6, 5400, 8, "Fiction", "German", [2017, 2020]),
    ("Il nome della rosa", "Umberto Eco", 4.6, 6200, 15, "Fiction", "Italian", [2015, 2019]),
    ("L'amica geniale (Neapolitan Novels)", "Elena Ferrante", 4.6, 8900, 16, "Fiction", "Italian", [2016, 2017, 2018]),

    # Cookbooks, Diet, and Specialized Language Titles
    ("Ina Garten of Modern Comfort Food: A Barefoot Contessa Cookbook", "Ina Garten", 4.8, 17000, 21, "Non Fiction", "English", [2020]),
    ("Salt, Fat, Acid, Heat: Mastering the Elements of Good Cooking", "Samin Nosrat", 4.8, 21000, 20, "Non Fiction", "English", [2018, 2019]),
    ("The Pioneer Woman Cooks: Dinnertime - Comfort Classics, Freezer Meals, 16-Minute Meals", "Ree Drummond", 4.8, 3428, 14, "Non Fiction", "English", [2015]),
    ("Thug Kitchen: The Official Cookbook: Eat Like You Give a F*ck", "Thug Kitchen", 4.6, 11128, 15, "Non Fiction", "English", [2014, 2015, 2016]),
    ("The Whole30: The 30-Day Guide to Total Health and Food Freedom", "Melissa Hartwig Urban", 4.6, 7508, 16, "Non Fiction", "English", [2015, 2016, 2017]),
    ("The Keto Diet: The Complete Guide to a High-Fat Diet", "Leanne Vogel", 4.6, 6800, 22, "Non Fiction", "English", [2017, 2018]),
    ("Medical Medium Liver Rescue: Answers to Eczema, Psoriasis, Diabetes, Strep, Acne, Gout", "Anthony William", 4.8, 6386, 22, "Non Fiction", "English", [2018, 2019]),

    # Politics, Journalism & Current Events
    ("Fire and Fury: Inside the Trump White House", "Michael Wolff", 4.2, 13677, 6, "Non Fiction", "English", [2018]),
    ("Fear: Trump in the White House", "Bob Woodward", 4.4, 6042, 2, "Non Fiction", "English", [2018]),
    ("Too Much and Never Enough: How My Family Created the World's Most Dangerous Man", "Mary L. Trump Ph.D.", 4.6, 62000, 16, "Non Fiction", "English", [2020]),
    ("The Room Where It Happened: A White House Memoir", "John Bolton", 4.3, 24000, 17, "Non Fiction", "English", [2020]),
    ("Rage", "Bob Woodward", 4.5, 18000, 18, "Non Fiction", "English", [2020]),
    ("Midnight in Chernobyl: The Untold Story of the World's Greatest Nuclear Disaster", "Adam Higginbotham", 4.7, 12000, 18, "Non Fiction", "English", [2019, 2020]),
    ("Say Nothing: A True Story of Murder and Memory in Northern Ireland", "Patrick Radden Keefe", 4.7, 14000, 17, "Non Fiction", "English", [2019, 2020])
]

def generate_dataset():
    records = []
    for title, author, rating, reviews, price, genre, lang, years in BOOK_CATALOG:
        for yr in years:
            # Vary reviews slightly by year to model growth over time
            yr_offset = yr - min(years)
            rev_adj = int(reviews * (0.85 + 0.15 * (yr_offset + 1) / len(years)))
            records.append({
                "Name": title,
                "Author": author,
                "User Rating": round(rating, 2),
                "Reviews": rev_adj,
                "Price": price,
                "Year": yr,
                "Genre": genre,
                "Language": lang
            })

    # Sort by Year and Reviews descending
    records.sort(key=lambda r: (r["Year"], -r["Reviews"]))

    fieldnames = ["Name", "Author", "User Rating", "Reviews", "Price", "Year", "Genre", "Language"]
    os.makedirs(os.path.dirname(DATASET_PATH), exist_ok=True)
    with open(DATASET_PATH, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"Generated {len(records)} records in {DATASET_PATH}")
    return records

if __name__ == "__main__":
    generate_dataset()
