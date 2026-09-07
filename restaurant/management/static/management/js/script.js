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
    },
    create: function(input, callback) {
        fetch(createIngredientUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken
            },
            body: 'name=' + encodeURIComponent(input)
        })
            .then(response => response.json())
            .then(data => {
                if (data.id && data.name) {
                    callback(data);
                } else {
                    callback();
                }
            })
            .catch(() => {
                callback();
            });
        }
});
select.clearOptions();
console.log("¡Script cargado correctamente!");