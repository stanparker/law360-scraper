var _ = require('underscore')
var fs = require('fs');
var jsonfile = require('jsonfile')
var converter = require('json-2-csv')

var obj;

fs.readFile('law_cases.json', 'utf8', function (err, data) {
  if (err) throw err;
  
  obj = JSON.parse(data);

  var groups = _.groupBy(obj, function(value, key, list){
  	
  	return value.district
  
  });

  var data = _.map(groups, function(group) {
  	return {
  		district: group[0].district,
  		cases: _.pluck(group, 'cases')
  	}
  })

  var options = {
    delimiter: {
      field : ',',
      array: '; '
    }
  }

  converter.json2csv(data, function(err, csv) {
    
    fs.writeFile('district_cases.csv', csv)

  }, options)

});

fs.unlinkSync('law_cases.json')


