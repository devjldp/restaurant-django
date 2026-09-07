const select = new TomSelect('#id_ingredients', {
    plugins: ['remove_button'],

    valueField: 'id',
    labelField: 'name',
    searchField: ['name'],

    placeholder: 'Search ingredients...',

    shouldLoad: function(query) {
        return query.length >= 2;
    },

    load: function(query, callback) {
        fetch(searchIngredientsUrl + "?q=" + encodeURIComponent(query))
            .then(response => response.json())
            .then(data => {callback(data);})
            .catch(() => {callback();});
    }
});
select.clearOptions();
console.log("¡Script cargado correctamente!");