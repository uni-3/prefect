import dlt
from prefect import task

from dlt_project.pokemon.pokeapi import pokemon_species

# pokemon to motherduck
@task(name="pokemon_to_motherduck", log_prints=True)
def load_task():
    pipeline = dlt.pipeline(
        pipeline_name='poke',
        #destination='filesystem',
        destination='motherduck',
        dataset_name='pokemon'
    )

    # init endpoint
    # 
    # pokemon pokemon-speciesとたどると、ポケモン一覧と詳細が取れる
    # pagerつきのリストがとれる
    poke_url = "https://pokeapi.co/api/v2/pokemon/"
    load_info = pipeline.run(pokemon_species(poke_url), loader_file_format="parquet")
    print(f"Incremental Load Customers Information: {load_info}")
    # verify that all went well
    row_counts = pipeline.last_trace.last_normalize_info.row_counts
    print(f"row count: {row_counts}")
