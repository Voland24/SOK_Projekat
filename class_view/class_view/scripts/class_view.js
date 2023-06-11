function display_graph(nodes, links) {
    links.forEach(function (link) {
        link.source = nodes[link.source];
        link.target = nodes[link.target];
    });

    var svg_node = d3.select('.svgClass').node();
    var width = svg_node.getBoundingClientRect().width;
    var height = svg_node.getBoundingClientRect().height;
    var force = d3.layout.force()                           //kreiranje force layout-a
        .size([width, height])                     //raspoloziv prostor za iscrtavanje
        .nodes(d3.values(nodes))                  //dodaj nodove
        .links(links)                             //dodaj linkove
        .on("tick", tick)                         //sta treba da se desi kada su izracunate nove pozicija elemenata
        .linkDistance(300)                        //razmak izmedju elemenata
        .charge(-100000)                           //koliko da se elementi odbijaju
        .start();                                 //pokreni izracunavanje pozicija

    var svg = d3.select('#ceoGraf');

    //Dodavanje linkova
    var link = svg.selectAll('.link')
        .data(force.links())
        .enter().append('line')
        .attr('class', 'link')
        .attr('stroke', '#9A9A9A')
        .attr('stroke-width', '3');


    // Dodavanje cvorova
    var node = svg.selectAll('.node')
        .data(force.nodes())
        .enter()
        .append('g')
        .attr('class', 'node')
        .attr('id', function (d) {
            return 'a' + d.id;
        });

    d3.selectAll('.node').each(function (d) {
        class_view(d);
    });
    width = 0;

    function get_tex_width(txt, font) {
        this.element = document.createElement('canvas');
        this.context = this.element.getContext("2d");
        this.context.font = font;
        return this.context.measureText(txt).width;
    }

    function class_view(d) {
        var j = 1;
        var str_len = 0;
        var str_text = "";

        var name_len = get_tex_width(d.element.name, '10px sans-serif');

        d3.select("g#" + 'a' + d.id)
            .append('rect').attr('class', 'rect_class')
            .attr('id', function (d) {
                return "rect_" + d.id
            })
            .attr('x', 0).attr('y', 0);

        var i = 0;
        var text_size = 10;

        for (let k in d.element) {
            j += 1;
            if ((d.element[k] + k).length > str_len) {
                str_text = d.element[k] + k + "  :  ";
                str_len = (d.element[k] + k).length;
            }
            if (k != "name") {
                i += 1;
                d3.select("g#" + 'a' + d.id)
                    .append('text')
                    .attr('x', 2).attr('y', 15 + i * text_size)
                    .attr('text-anchor', 'start')
                    .attr('font-size', text_size).attr('font-family', 'sans-serif')
                    .attr('fill', '#E6E6E6').text(k + " : " + d.element[k]);
            }
        }

        width = get_tex_width(str_text, '10px sans-serif');

        var height = j * 10;

        d3.select("#rect_" + d.id).attr('width', width).attr('height', height)
            .style('fill', '#B985FA')
            .attr('stroke', '#9A9A9A')
            .attr('stroke-width', '2');

        d3.select("g#" + 'a' + d.id)
            .append('text')
            .style("text-anchor", "right")
            .attr('x', width / 2 - name_len / 2).attr('y', text_size)
            .attr('font-size', '10px')
            .attr('font-family', 'sans-serif')
            .attr('fill', '#E6E6E6').text(d.element.name);

        d3.select("g#" + 'a' + d.id)
            .append('line')
            .attr('x1', 0).attr('y1', text_size + 5)
            .attr('x2', width).attr('y2', text_size + 5)
            .attr('stroke', '#9A9A9A').attr('stroke-width', 1);
    }

    function tick(e) {
        node.attr("transform", function (d) {
            return "translate(" + d.x + "," + d.y + ")";
        })
            .call(force.drag);

        link.attr('x1', function (d) {
            var width = d3.select("#rect_" + d.source.id).attr("width");
            return d.source.x + width / 2;
        })
            .attr('y1', function (d) {
                return d.source.y;
            })
            .attr('x2', function (d) {
                var width = d3.select("#rect_" + d.target.id).attr("width");
                return d.target.x + width / 2;
            })
            .attr('y2', function (d) {
                return d.target.y;
            });

        $('#birdDisplay').html($('#bigDisplay').html());
        var gr = $('#birdDisplay .graphy');
        gr.attr('transform', 'matrix(0.02 0 0 0.02 100 100)');
    }

    select_in_graph = function () {
        let graph_node = document.getElementById('rect_' + window.selected_node_id);
        graph_node.style.fill = '#f70776';
    }

    deselect_in_graph = function () {
        let nodee = document.getElementById('rect_' + window.selected_node_id);
        if (nodee) {
            nodee.style.fill = '#B985FA'
        }
    }
}
