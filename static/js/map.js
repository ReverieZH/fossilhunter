 var myChart = echarts.init(document.getElementById('main'));
    myChart.setOption({
    bmap: {
        center: [109.5996,35.7396],
        zoom: 6,
        roam: true,

    },
    series: [{
        type: 'scatter',
        coordinateSystem: 'bmap',
        data: [ [120, 30, 1] ]
    }]


});

var bmap = myChart.getModel().getComponent('bmap').getBMap();
bmap.addControl(new BMap.MapTypeControl());
bmap.setMapStyleV2({
        styleId:'443bf2439c3ec063ba3c646f29deaff0'
    })