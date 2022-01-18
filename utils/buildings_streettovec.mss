@building-fill: #d9d0c9;  // Lch(84, 5, 68)
@building-line: darken(@building-fill, 15%);  // Lch(70, 9, 66)
@building-low-zoom: darken(@building-fill, 4%);

// Colormap generated by https://colorbrewer2.org 9 classes Greys
@building-1c: #ffffff; // Not used 
@building-2c: #f0f0f0;
@building-3c: #d9d9d9;
@building-4c: #bdbdbd;
@building-5c: #969696;
@building-6c: #737373;
@building-7c: #525252;
@building-8c: #252525;
@building-9c: #000000;

@building-major-fill: darken(@building-fill, 10%);  // Lch(75, 8, 67)
@building-major-line: darken(@building-major-fill, 15%);  // Lch(61, 13, 65)
@building-major-z15: darken(@building-major-fill, 5%);  // Lch(70, 9, 66)
@building-major-z14: darken(@building-major-fill, 10%);  // Lch(66, 11, 65)

@entrance-permissive: darken(@building-line, 15%);
@entrance-normal: @building-line;

#buildings {
  [zoom >= 14] {
    polygon-fill: @building-low-zoom;
    polygon-clip: false;
    [zoom >= 15] {
      polygon-fill: @building-2c;
      line-color: @building-line;
      line-width: .75;
      line-clip: false;
      
      [height >= 3.0]{
            polygon-fill: @building-3c;
      }
      [height >= 6.0]{
            polygon-fill: @building-4c;
      }
      [height >= 9.0]{
            polygon-fill: @building-5c;
      }
      [height >= 12.0]{
            polygon-fill: @building-6c;
      }
      [height >= 18.0]{
            polygon-fill: @building-7c;
      }
      [height >= 24.0]{
            polygon-fill: @building-8c;
      }
      [height >= 30.0]{
            polygon-fill: @building-9c;
      }
      /*
      [height >= 60.0]{
            polygon-fill: @building-9c;
      }
      */
      
      
    }


    /* [amenity = 'place_of_worship'],
    [aeroway = 'terminal'],
    [aerialway = 'station'],
    [building = 'train_station'],
    [public_transport = 'station'] {
      polygon-fill: @building-major-z14;
      [zoom >= 15] {
        polygon-fill: @building-major-z15;
        line-color: @building-major-line;
        [zoom >= 16] {
          polygon-fill: @building-major-fill;
        }
      } 
    }*/
  }
}

#bridge {
  [zoom >= 12] {
    polygon-fill: #B8B8B8;
  }
}

#entrances {
  [zoom >= 18]["entrance" != null]  {
    marker-fill: @entrance-normal;
    marker-allow-overlap: true;
    marker-ignore-placement: true;
    marker-file: url('symbols/rect.svg');
    marker-width: 5.0;
    marker-height: 5.0;
    marker-opacity: 0.0;
    ["entrance" = "main"] {
      marker-opacity: 1.0;
      marker-file: url('symbols/square.svg');
    }
  }
  [zoom >= 19]["entrance" != null] {
    ["entrance" = "yes"],
    ["entrance" = "main"],
    ["entrance" = "home"],
    ["entrance" = "service"],
    ["entrance" = "staircase"] {
      marker-opacity: 1.0;
      marker-width: 6.0;
      marker-height: 6.0;
      ["entrance" = "service"] {
        marker-file: url('symbols/corners.svg');
      }
    }
    ["access" = "yes"],
    ["access" = "permissive"] {
      marker-fill: @entrance-permissive;
    }
    ["access" = "no"] {
      marker-fill: @entrance-normal;
      marker-file: url('symbols/rectdiag.svg');
    }
  }
  [zoom >= 20]["entrance" != null] {
    marker-width: 8.0;
    marker-height: 8.0;
  }
}
