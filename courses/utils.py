# efface les enregistrements de plusieurs tables
# prend un tableau en argument
def clear_tables(models):
    for model in models:
        model.objects.all().delete()