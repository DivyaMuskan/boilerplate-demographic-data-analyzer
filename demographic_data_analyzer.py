import pandas as pd


def calculate_demographic_data(print_data=True):
    df = pd.read_csv("adult.data.csv", skipinitialspace=True)

    
    # Remove leading and trailing spaces from text columns
    for column in df.select_dtypes(include="object").columns:
        df[column] = df[column].str.strip()

    # How many of each race are represented?
    race_count = df["race"].value_counts()

    # Average age of men
       
    df["age"] = pd.to_numeric(df["age"], errors="coerce")
    average_age_men = round(
        df.loc[df["sex"] == "Male", "age"].mean(), 1
    )

    # Percentage with a Bachelor's degree
    percentage_bachelors = round(
        (df["education"] == "Bachelors").mean() * 100, 1
    )

    # Higher and lower education
    higher_education = df["education"].isin(
        ["Bachelors", "Masters", "Doctorate"]
    )
    lower_education = ~higher_education

    # Percentage of people with higher education earning >50K
    higher_education_rich = round(
        (df.loc[higher_education, "salary"] == ">50K").mean() * 100, 1
    )

    # Percentage of people without higher education earning >50K
    lower_education_rich = round(
        (df.loc[lower_education, "salary"] == ">50K").mean() * 100, 1
    )

    # Minimum work hours per week
    min_work_hours = df["hours-per-week"].min()

    # Percentage of people working minimum hours who earn >50K
    min_workers = df[df["hours-per-week"] == min_work_hours]
    num_min_workers = len(min_workers)

    rich_percentage = round(
        (min_workers["salary"] == ">50K").mean() * 100, 1
    )

    # Country with the highest percentage earning >50K
    rich_by_country = df.assign(
        rich=(df["salary"] == ">50K")
    ).groupby("native-country")["rich"].mean()

    highest_earning_country = rich_by_country.idxmax()
    highest_earning_country_percentage = round(
        rich_by_country.max() * 100, 1
    )

    # Most popular occupation in India among people earning >50K
    top_IN_occupation = (
        df.loc[
            (df["native-country"] == "India")
            & (df["salary"] == ">50K"),
            "occupation"
        ]
        .value_counts()
        .idxmax()
    )

    if print_data:
        print("Number of each race:\n", race_count)
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(
            "Percentage with higher education that earn >50K: "
            f"{higher_education_rich}%"
        )
        print(
            "Percentage without higher education that earn >50K: "
            f"{lower_education_rich}%"
        )
        print(f"Min work time: {min_work_hours} hours/week")
        print(
            "Percentage of rich among those who work fewest hours: "
            f"{rich_percentage}%"
        )
        print("Country with highest percentage of rich:", highest_earning_country)
        print(
            "Highest percentage of rich people in country: "
            f"{highest_earning_country_percentage}%"
        )
        print("Top occupations in India:", top_IN_occupation)

    return {
        "race_count": race_count,
        "average_age_men": average_age_men,
        "percentage_bachelors": percentage_bachelors,
        "higher_education_rich": higher_education_rich,
        "lower_education_rich": lower_education_rich,
        "min_work_hours": min_work_hours,
        "num_min_workers": num_min_workers,
        "rich_percentage": rich_percentage,
        "highest_earning_country": highest_earning_country,
        "highest_earning_country_percentage": highest_earning_country_percentage,
        "top_IN_occupation": top_IN_occupation,
    }
