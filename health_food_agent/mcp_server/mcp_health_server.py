from mcp.server.fastmcp import FastMCP
import requests
import urllib.parse

mcp = FastMCP("Health-Service")

storage = {
    "steps": 0,
    "meals": []
}


@mcp.tool()
def get_calories(food: str) -> str:
    """Fetch calorie data from Open Food Facts."""
    food_name = food.lower().strip()
    try:
        response = requests.get(
            "https://world.openfoodfacts.org/cgi/search.pl",
            params={
                "search_terms": food_name,
                "search_simple": 1,
                "action": "process",
                "json": 1,
                "page_size": 30,
                "fields": "product_name,generic_name,nutriments",
            },
            timeout=15,
        )
        data = response.json()
        products = data.get("products", [])

        if not products:
            return f"找不到 {food} 的卡路里資料。"

        checked = []
        for product in products:
            product_name = product.get("product_name") or ""
            generic_name = product.get("generic_name") or ""
            name = product_name or generic_name or food

            nutriments = product.get("nutriments", {})
            kcal = (
                nutriments.get("energy-kcal_100g")
                or nutriments.get("energy-kcal")
                or nutriments.get("energy-kcal_value")
            )
            checked.append(name)
            if kcal is not None:
                return f"{name} 每 100 克約含有 {kcal} 大卡 (kcal)。"

        return f"找不到 {food} 的確切熱量。有查到類似的：{', '.join(checked[:5])}"
    except Exception as error:
        return f"API 查詢失敗：{error}"


@mcp.tool()
def log_meal(food_name: str, calories: int) -> str:
    """Log a meal that the user has eaten today."""
    storage["meals"].append({"food": food_name, "calories": calories})
    return f"成功記錄！你吃了 {food_name}，熱量 {calories} 大卡。"


@mcp.tool()
def get_daily_summary() -> str:
    """Get the summary of meals eaten today and total calories."""
    if not storage["meals"]:
        return "你今天還沒記錄任何食物！"
    
    total_cal = sum(item["calories"] for item in storage["meals"])
    food_list = ", ".join(f"{item['food']} ({item['calories']} kcal)" for item in storage["meals"])
    return f"今日總熱量: {total_cal} 大卡。吃了這些東西: {food_list}。"


@mcp.tool()
def calculate_bmi(weight_kg: float, height_cm: float) -> str:
    """Calculate BMI and return the category."""
    if height_cm <= 0 or weight_kg <= 0:
        return "身高和體重必須大於 0 哦！"
    
    height_m = height_cm / 100
    bmi = round(weight_kg / (height_m * height_m), 1)
    
    if bmi < 18.5:
        category = "體重過輕 (Underweight)"
    elif 18.5 <= bmi < 24:
        category = "正常範圍 (Normal weight)"
    elif 24 <= bmi < 27:
        category = "過重 (Overweight)"
    elif 27 <= bmi < 30:
        category = "輕度肥胖 (Obese Class I)"
    elif 30 <= bmi < 35:
        category = "中度肥胖 (Obese Class II)"
    else:
        category = "重度肥胖 (Obese Class III)"
        
    return f"你的 BMI 是 {bmi}，屬於：{category}。"


@mcp.tool()
def get_recipe(ingredient: str, cuisine: str = "") -> str:
    """Fetch recipe ideas from TheMealDB."""
    ingredient = ingredient.lower().strip()
    cuisine = cuisine.strip()
    try:
        ingredient_response = requests.get(
            "https://www.themealdb.com/api/json/v1/1/filter.php",
            params={"i": ingredient},
            timeout=10,
        ).json()

        if ingredient_response.get("meals"):
            meals = ingredient_response["meals"][:3]
            names = ", ".join(meal["strMeal"] for meal in meals)
            return f"使用 {ingredient} 的食譜靈感：{names}"

        search_response = requests.get(
            "https://www.themealdb.com/api/json/v1/1/search.php",
            params={"s": ingredient},
            timeout=10,
        ).json()

        if search_response.get("meals"):
            meals = search_response["meals"][:3]
            names = ", ".join(meal["strMeal"] for meal in meals)
            return f"與 {ingredient} 相關的食譜：{names}"

        if cuisine:
            cuisine_response = requests.get(
                "https://www.themealdb.com/api/json/v1/1/filter.php",
                params={"a": cuisine},
                timeout=10,
            ).json()

            if cuisine_response.get("meals"):
                meals = cuisine_response["meals"][:3]
                names = ", ".join(meal["strMeal"] for meal in meals)
                return f"找不到 {ingredient}，但這裡有一些 {cuisine} 料理靈感：{names}"

        return f"找不到 {ingredient} 的食譜。試試雞肉、雞蛋、牛肉或義大利麵吧！"
    except Exception as error:
        return f"API 查詢失敗：{error}"


@mcp.tool()
def search_youtube_recipe(dish_name: str) -> str:
    """Get a YouTube search link for a recipe."""
    query = urllib.parse.quote(f"how to cook {dish_name} recipe")
    return f"https://www.youtube.com/results?search_query={query}"


@mcp.tool()
def manage_steps(action: str, value: int = 0) -> str:
    """Manage step count. action can be add, get, or reset."""
    action = action.lower().strip()

    if action == "add":
        if value <= 0:
            return "步數必須是大於 0 的數字！"
        storage["steps"] += value
        return f"增加了 {value} 步！目前總步數：{storage['steps']} 步。"

    if action == "get":
        return f"目前的步數：{storage['steps']} 步。"

    if action == "reset":
        storage["steps"] = 0
        return "步數已經歸零重置。"

    return "無效的操作，請使用 add, get 或 reset。"


if __name__ == "__main__":
    mcp.run()
