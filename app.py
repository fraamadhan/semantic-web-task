from SPARQLWrapper import SPARQLWrapper, JSON
from flask import Flask, render_template, request

app = Flask(__name__)

sparql_endpoint = "http://localhost:3030/data_sekolah_jawa_barat/query"  

def get_query(keyword=None):
    query = """
    PREFIX id: <https://dapo.kemdikbud.go.id/>
    PREFIX item: <https://dapo.kemdikbud.go.id/sp/item#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

    SELECT ?NamaSekolah ?Provinsi ?Kota ?Kec ?NPSN ?Status ?Sync ?Guru ?Pegawai
    WHERE {
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
                REGEX(LCASE(?Guru), "{keyword}", "i") ||
                REGEX(LCASE(?Pegawai), "{keyword}", "i")
            )
        '''
    query += "}"
    return query


def fetch_data(keyword=None):
    sparql = SPARQLWrapper(sparql_endpoint)
    sparql.setQuery(get_query(keyword))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()["results"]["bindings"]

    total_school = 0
    data = []
    for result in results:
        total_school += 1
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
    
    return data, total_school

@app.route("/")
def index():
    keyword = request.args.get('keyword')
    data, total_school = fetch_data(keyword)
    return render_template("index.html", data=data, total_school=total_school)

if __name__ == "__main__":
    app.run(debug=True)
