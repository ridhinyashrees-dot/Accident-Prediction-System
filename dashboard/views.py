from django.shortcuts import render, redirect
from .forms import AccidentForm
from django.contrib import messages
from .data import accident_data
from .db import collection



def home(request):

    # 🔥 Step 0: Get MongoDB data
    db_data = list(collection.find({}, {"_id": 0}))
    print("Mongo Data:",db_data)
    # 🔥 Combine default + DB
    all_data = accident_data + db_data

    # Step 1: Count accidents for each factor
    factor_counts = {}

    for accident in all_data:
        factor = accident["factor"]
        factor_counts[factor] = factor_counts.get(factor, 0) + 1

    total_accidents = len(all_data)

    # Step 2: Find factors with death cases
    death_factors = set()

    for accident in all_data:
        if accident["severity"] == "Death":
            death_factors.add(accident["factor"])

    # Step 3: Assign 30% death weight
    death_weight = {}
    if len(death_factors) > 0:
        weight_per_factor = 30 / len(death_factors)
        for factor in death_factors:
            death_weight[factor] = weight_per_factor

    # Step 4: Calculate 70% frequency weight
    frequency_weight = {}

    for factor, count in factor_counts.items():
        frequency_weight[factor] = (count / total_accidents) * 70

    # Step 5: Final risk score
    final_scores = {}

    for factor in factor_counts:
        final_scores[factor] = frequency_weight.get(factor, 0) + death_weight.get(factor, 0)

    # Step 6: Find most dangerous factor
    most_dangerous = max(final_scores, key=final_scores.get)

    # Step 7: Send to chart
    
    sorted_data = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)

    sorted_labels = [x[0] for x in sorted_data]
    sorted_values = [x[1] for x in sorted_data]

# 🎨 Assign colors based on ranking
    color_palette = ['#ff4d4d', '#ffd11a', '#3399ff', '#33cc33']

    colors = []

    for i in range(len(sorted_labels)):
        if i < len(color_palette):
           colors.append(color_palette[i])
        else:
           colors.append('#cccccc')

# ✅ Updated context
    context = {
        "labels": sorted_labels,
        "values": sorted_values,
        "colors": colors,
        "prediction": most_dangerous
    } 


    return render(request, "dashboard/home.html", context)


# 👉 FORM VIEW (NEW)
def form_page(request):
    form = AccidentForm()
    
    if request.method == "POST":
        form = AccidentForm(request.POST)
        if form.is_valid():
            new_data = {
                "vehicle": form.cleaned_data["vehicle"],
                "factor": form.cleaned_data["factor"],
                "severity": form.cleaned_data["severity"],
                "time": form.cleaned_data["time"]
            }

            collection.insert_one(new_data)
            
            messages.success(request, "Data submitted successfully!")

            return redirect('form_page')

    return render(request, "dashboard/forms.html", {"form": form})





