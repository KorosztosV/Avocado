class AvocadoRow:
    def __init__(self, row):
        self.date = row["Date"]
        self.average_price = float(row["AveragePrice"])
        self.total_volume = float(row["Total Volume"])
        self._4046 = float(row["4046"])
        self._4225 = float(row["4225"])
        self._4770 = float(row["4770"])
        self.total_bags = float(row["Total Bags"])
        self.small_bags = float(row["Small Bags"])
        self.large_bags = float(row["Large Bags"])
        self.xlarge_bags = float(row["XLarge Bags"])
        self.type = row["type"]
        self.year = int(row["year"])
        self.region = row["region"]

from google.colab import drive
drive.mount('/content/drive')



def read_avocado_data():
    import csv
    file_path = "/content/drive/MyDrive/gepi1/avocado.csv"
    with open(file_path, mode="r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        return [AvocadoRow(row) for row in reader if row["region"] != "TotalUS"]


def graph_price_demand(data):
    import matplotlib.pyplot as plt

    groups_by_date = {}
    for row in data:
        if row.date not in groups_by_date:
            groups_by_date[row.date] = {
                "total_volume": 0,
                "weighted_price": 0, 
            }

        groups_by_date[row.date]["total_volume"] += row.total_volume
        groups_by_date[row.date]["weighted_price"] += row.average_price * row.total_volume   # <-- súlyozás

    dates = sorted(groups_by_date.keys())
    total_volumes = [groups_by_date[date]["total_volume"] for date in dates]

    # Súlyozott átlagár kiszámítása
    average_prices = [
        groups_by_date[date]["weighted_price"] / groups_by_date[date]["total_volume"]
        for date in dates
    ]

    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax1.set_xlabel("Date")

    ax1.set_ylabel("Total Volume", color="tab:blue")
    ax1.plot(dates, total_volumes, color="tab:blue", label="Total Volume")
    ax1.tick_params(axis="y", labelcolor="tab:blue")
    plt.xticks(rotation=45, ha="right")

    ax2 = ax1.twinx()
    ax2.set_ylabel("Weighted Average Price", color="tab:orange")
    ax2.plot(dates, average_prices, color="tab:orange", label="Average Price")
    ax2.tick_params(axis="y", labelcolor="tab:orange")

    plt.title("Avocado Price and Demand Over Time")
    fig.tight_layout()
    plt.show()


def graph_bio_vs_normal(data):
    import matplotlib.pyplot as plt

    groups_by_region = {}
    for row in data:
        if row.region not in groups_by_region:
            groups_by_region[row.region] = {
                "organic_volume": 0,
                "conventional_volume": 0,
            }
        if row.type == "organic":
            groups_by_region[row.region]["organic_volume"] += row.total_volume
        else:
            groups_by_region[row.region]["conventional_volume"] += row.total_volume

    # Craete bar chart to compare organic vs conventional volumes by region
    regions = sorted(groups_by_region.keys())
    organic_volumes = [groups_by_region[region]["organic_volume"] for region in regions]
    conventional_volumes = [
        groups_by_region[region]["conventional_volume"] for region in regions
    ]

    x = range(len(regions))
    width = 0.35
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(x, organic_volumes, width, label="Organic", color="green")
    ax.bar(
        [xi + width for xi in x],
        conventional_volumes,
        width,
        label="Conventional",
        color="brown",
    )
    ax.set_xlabel("Region")
    ax.set_ylabel("Total Volume")
    ax.set_title("Organic vs Conventional Avocado Volumes by Region")
    ax.set_xticks([xi + width / 2 for xi in x])
    ax.set_xticklabels(regions, rotation=45, ha="right")
    ax.legend()
    plt.tight_layout()
    plt.show()



def graph_price_by_month(data):
    import matplotlib.pyplot as plt
    import datetime

    groups_by_month = {}
    for row in data:
        month = datetime.datetime.strptime(row.date, "%Y-%m-%d").strftime("%Y-%m")
        if month not in groups_by_month:
            groups_by_month[month] = {"total_weighted_price": 0, "total_volume": 0}

        # Súlyozott ár
        groups_by_month[month]["total_weighted_price"] += row.average_price * row.total_volume
        groups_by_month[month]["total_volume"] += row.total_volume

    months = sorted(groups_by_month.keys())
    average_prices = [
        groups_by_month[month]["total_weighted_price"] / groups_by_month[month]["total_volume"]
        for month in months
    ]

    fig, ax = plt.subplots(figsize=(12, 6))

    # Define season colors
    season_colors = {
        "winter": "#FFFFFF",   # white
        "spring": "#90EE90",   # light green
        "summer": "#FFFF99",   # yellow
        "fall": "#FFB366",     # orange
    }

    # Add seasonal backgrounds
    for i, month in enumerate(months):
        month_num = int(month.split("-")[1])
        if month_num in [12, 1, 2]:
            color = season_colors["winter"]
        elif month_num in [3, 4, 5]:
            color = season_colors["spring"]
        elif month_num in [6, 7, 8]:
            color = season_colors["summer"]
        else:
            color = season_colors["fall"]

        ax.axvspan(i - 0.5, i + 0.5, facecolor=color, alpha=0.3)

    ax.plot(range(len(months)), average_prices, marker="o", color="darkblue", linewidth=2)
    ax.set_xlabel("Month")
    ax.set_ylabel("Weighted Average Price")
    ax.set_title("Weighted Average Avocado Price by Month")
    ax.set_xticks(range(len(months)))
    ax.set_xticklabels(months, rotation=45, ha="right")
    plt.tight_layout()
    plt.show()




def graph_bio_size_relation(data: list[AvocadoRow]):
    import matplotlib.pyplot as plt

    # Adatok előkészítése
    organic_sizes = {"_4046": [], "_4225": [], "_4770": []}
    conventional_sizes = {"_4046": [], "_4225": [], "_4770": []}

    for row in data:
        if row.type == "organic":
            organic_sizes["_4046"].append(row._4046)
            organic_sizes["_4225"].append(row._4225)
            organic_sizes["_4770"].append(row._4770)
        else:
            conventional_sizes["_4046"].append(row._4046)
            conventional_sizes["_4225"].append(row._4225)
            conventional_sizes["_4770"].append(row._4770)

    size_labels = ["_4046", "_4225", "_4770"]
    organic_means = [sum(organic_sizes[size])/len(organic_sizes[size]) for size in size_labels]
    conventional_means = [sum(conventional_sizes[size])/len(conventional_sizes[size]) for size in size_labels]

    # Ábra készítése
    x = range(len(size_labels))
    width = 0.35
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(x, organic_means, width, label="Organic", color="green")
    ax.bar([xi + width for xi in x], conventional_means, width, label="Conventional", color="brown")

    # Xticks a két sáv közepére
    ax.set_xticks([xi + width/2 for xi in x])
    ax.set_xticklabels(size_labels)

    ax.set_xlabel("Avocado Size")
    ax.set_ylabel("Average Volume")
    ax.set_title("Average Avocado Size Volume: Organic vs Conventional")
    ax.legend(title="Type")

    plt.tight_layout()
    plt.show()

    # Visszaadjuk az értékeket további felhasználáshoz
    return size_labels, organic_means, conventional_means




import matplotlib.patches as mpatches

def graph_sales_by_size_by_region(data):
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches

    regions = {}
    for row in data:
        if row.region not in regions:
            regions[row.region] = {"_4046": 0, "_4225": 0, "_4770": 0}
        regions[row.region]["_4046"] += row._4046
        regions[row.region]["_4225"] += row._4225
        regions[row.region]["_4770"] += row._4770

    size_labels = ["_4046", "_4225", "_4770"]
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]  # egyedi, jól elkülöníthető színek
    x = range(len(regions))
    width = 0.2
    num_sizes = len(size_labels)

    fig, ax = plt.subplots(figsize=(12, 6))
    for i, (size, color) in enumerate(zip(size_labels, colors)):
        size_volumes = [regions[region][size] for region in regions]
        ax.bar([xi + i * width for xi in x], size_volumes, width, color=color)

    # Középre állítjuk az xticks-et
    ax.set_xticks([xi + width*(num_sizes-1)/2 for xi in x])
    ax.set_xticklabels(regions.keys(), rotation=45, ha="right")

    ax.set_xlabel("Region")
    ax.set_ylabel("Total Volume Sold")
    ax.set_title("Total Avocado Sales by Size and Region")

    # Legend manuálisan
    patches = [mpatches.Patch(color=color, label=size) for size, color in zip(size_labels, colors)]
    ax.legend(handles=patches, title="Avocado Size", bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    plt.show()





import matplotlib.pyplot as plt
if __name__ == "__main__":
    data = read_avocado_data()

    graph_price_demand(data)
    graph_bio_vs_normal(data)
    graph_price_by_month(data)
    graph_bio_size_relation(data)
    graph_sales_by_size_by_region(data)
