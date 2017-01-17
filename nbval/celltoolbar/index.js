// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


define([
    'notebook/js/celltoolbar',
], function(celltoolbar) {
    "use strict";

    var CellToolbar = celltoolbar.CellToolbar;

    var nbval_preset = [];

    var checkbox_test = CellToolbar.utils.checkbox_ui_generator('Check outputs',
         // setter
         function(cell, value){
             // we check that the nbval namespace exist and create it if needed
             if (cell.metadata.nbval === undefined) {
                 cell.metadata.nbval = {};
             }
             // set the value
             cell.metadata.nbval.compare_outputs = value;
             },
         // getter
         function(cell){
             var ns = cell.metadata.nbval;
             // if the slideshow namespace does not exist return `undefined`
             // (will be interpreted as `false` by checkbox) otherwise
             // return the value
             return (ns === undefined) ? undefined: ns.compare_outputs;
             }
    );


    var load_ipython_extension = function () {
        CellToolbar.register_callback('nbval.compare_outputs', checkbox_test, ['code']);
        nbval_preset.push('nbval.compare_outputs');

        CellToolbar.register_preset('Nbval', nbval_preset);
        console.log('Extension for setting nbval cell metadata.');
    };
    return {'load_ipython_extension': load_ipython_extension};
});
