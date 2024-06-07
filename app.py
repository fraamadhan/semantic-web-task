from SPARQLWrapper import SPARQLWrapper, JSON
from flask import Flask, render_template, request

app = Flask(__name__)

sparql_endpoint = "http://localhost:3030/data_sekolah_jawa_barat/query"  

def get_query(keyword=None, limit=10, offset=0):
    query = f"""
    PREFIX id: <https://dapo.kemdikbud.go.id/>
    PREFIX item: <https://dapo.kemdikbud.go.id/sp/item#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

    SELECT ?NamaSekolah ?Provinsi ?Kota ?Kec ?NPSN ?Status ?Sync ?Guru ?Pegawai
    WHERE {{
        ?items
            item:NamaSekolah    ?NamaSekolah ;
            item:Provinsi       ?Provinsi ;
            item:Kota           ?Kota ;
            item:Kec            ?Kec ;
            item:NPSN           ?NPSN ;
            item:Status         ?Status ;
            item:Sync           ?Sync ;
            item:Guru           ?Guru ;
            item:Pegawai        ?Pegawai .
    """
    if keyword:
        keyword = keyword.replace(" ", ".")
        query += f'''
            FILTER (
                REGEX(LCASE(?NamaSekolah), "{keyword}", "i") ||
                REGEX(LCASE(?Provinsi), "{keyword}", "i") ||
                REGEX(LCASE(?Kota), "{keyword}", "i") ||
                REGEX(LCASE(?Kec), "{keyword}", "i") ||
                REGEX(LCASE(?Sync), "{keyword}", "i") ||
                REGEX(LCASE(?NPSN), "{keyword}", "i") ||
                REGEX(LCASE(?Status), "{keyword}", "i") ||
                REGEX(LCASE(?Guru), "{keyword}", "i") ||
                REGEX(LCASE(?Pegawai), "{keyword}", "i")
            )
        '''
    query += f"}} LIMIT {limit} OFFSET {offset}"
    return query

def fetch_data(keyword=None, page=1, limit=10):
    offset = (page - 1) * limit
    sparql = SPARQLWrapper(sparql_endpoint)
    sparql.setQuery(get_query(keyword, limit, offset))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()["results"]["bindings"]

    data = []
    for result in results:
        data.append({
            'NamaSekolah': result['NamaSekolah']['value'],
            'Provinsi': result['Provinsi']['value'],
            'Kota': result['Kota']['value'],
            'Kec': result['Kec']['value'],
            'NPSN': result['NPSN']['value'],
            'Status': result['Status']['value'],
            'Sync': result['Sync']['value'],
            'Guru': result['Guru']['value'],
            'Pegawai': result['Pegawai']['value']
        })
    
    sparql.setQuery(get_query(keyword, limit=1000000, offset=0))  
    total_results = sparql.query().convert()["results"]["bindings"]
    total_school = len(total_results)

    return data, total_school

@app.route("/")
def index():
    keyword = request.args.get('keyword')
    page = int(request.args.get('page', 1))
    limit = 10
    data, total_school = fetch_data(keyword, page, limit)
    total_pages = (total_school + limit - 1) / limit

    return render_template("index.html", data=data, total_school=total_school, total_pages=int(total_pages), current_page=page)

if __name__ == "__main__":
    app.run(debug=True)
