# src/pokemon/pokeapi.py 
import dlt
from dlt.sources.helpers import requests


@dlt.source(max_table_nesting=2)
def pokemon_species(pokemon_api_url: str):
    # note that we deselect `pokemon_list` - we do not want it to be loaded
    @dlt.resource(table_name="pokemon", selected=False,
                  write_disposition="merge", primary_key="id")
    def pokemon_list():
        """Retrieve a first page of Pokemons and yield it. We do not retrieve all the pages in this example"""
        next_url = pokemon_api_url
        while next_url:
            response = requests.get(next_url).json()
            yield response["results"]
            next_url = response.get("next")

            # yield 動作確認 1回目のみ
            break

    # transformer that retrieves a list of objects in parallel
    @dlt.transformer
    def pokemon(pokemons):
        """Yields details for a list of `pokemons`"""

        # @dlt.defer marks a function to be executed in parallel
        # in a thread pool
        @dlt.defer
        def _get_pokemon(_pokemon):
            return requests.get(_pokemon["url"]).json()

        # call and yield the function result normally, the @dlt.defer takes care of parallelism
        for _pokemon in pokemons:
            yield _get_pokemon(_pokemon)

    # a special case where just one item is retrieved in transformer
    # a whole transformer may be marked for parallel execution
    @dlt.transformer(parallelized=True, write_disposition="merge", primary_key="id")
    def species(pokemon_details):
        """Yields species details for a pokemon"""
        species_data = requests.get(pokemon_details["species"]["url"]).json()
        # link back to pokemon so we have a relation in loaded data
        species_data["pokemon_id"] = pokemon_details["id"]
        # You can return the result instead of yield since the transformer only generates one result
        return species_data

    # create two simple pipelines with | operator
    # 1. send list of pokemons into `pokemon` transformer to get pokemon details
    # 2. send pokemon details into `species` transformer to get species details
    # NOTE: dlt is smart enough to get data from pokemon_list and pokemon details once

    # dltのpipeline構文
    return (pokemon_list | pokemon, pokemon_list | pokemon | species)


if __name__ == "__main__":
    print("deploy dlt")

    pipeline = dlt.pipeline(
        pipeline_name='poke',
        destination='motherduck',
        dataset_name='main',
        dev_mode=False,
    )

    # init endpoint
    # 
    # pokemon pokemon-speciesとたどると、ポケモン一覧と詳細が取れる
    # pagerつきのリストがとれる
    poke_url = "https://pokeapi.co/api/v2/pokemon/"
    load_info = pipeline.run(pokemon_species(poke_url), loader_file_format="parquet")
    # display where the data went
    print(load_info)