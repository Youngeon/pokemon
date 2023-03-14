import aiohttp
import asyncio
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/pokemon')
async def list_pokemon_names():
    async with aiohttp.ClientSession() as session:
        pokemon_url = 'https://pokeapi.co/api/v2/pokemon?limit=2000'
        async with session.get(pokemon_url) as resp:
            pokemon_list = await resp.json()
            count = pokemon_list['count']
            names = [pokemon['name'] for pokemon in pokemon_list['results']]
            names.append(count)
            return jsonify(names)
        
@app.route('/pokemon/<name>')
async def get_pokemon_by_name(name):
    async with aiohttp.ClientSession() as session:
        pokemon_url = f'https://pokeapi.co/api/v2/ability/{name}'
        async with session.get(pokemon_url) as resp:
            pokemon = await resp.json()
            return jsonify(pokemon)

@app.route('/pokemon/types/<type_name>')
async def get_pokemon_by_type(type_name):
    async with aiohttp.ClientSession() as session:
        pokemon_url = f'https://pokeapi.co/api/v2/type/{type_name}'
        async with session.get(pokemon_url) as resp:
            pokemon_type = await resp.json()
            pokemon_list = []
            for pokemon in pokemon_type['pokemon']:
                pokemon_url = pokemon['pokemon']['url']
                async with session.get(pokemon_url) as resp:
                    pokemon_data = await resp.json()
                    pokemon_list.append(pokemon_data)
            return jsonify(pokemon_list)

if __name__ == '__main__':
    app.run(debug=True)
