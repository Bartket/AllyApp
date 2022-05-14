<template>
  <div class="w-full h-full select-none" style="-webkit-tap-highlight-color: transparent;">
    <!-- Modal windows -->
    <location-modal :show="showLocationModal" @hide="showLocationModal = false" @save="addLocation"></location-modal>
    <title-modal :show="showTitleModal" @hide="saveTitle"></title-modal>

    <!-- Action button in the bottom left -->
    <div class="absolute bottom-2 left-2 sm:bottom-4 sm:left-4 z-20 flex">
      <action-button @click="showLocationModal = true">
        <svg class="svg-icon" style="width: 2em; height: 2em; vertical-align: middle;fill: currentColor;overflow: hidden;" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"><path d="M512 891.733333l211.2-211.2a298.666667 298.666667 0 1 0-422.4 0L512 891.733333z m0 120.661334l-271.530667-271.530667a384 384 0 1 1 543.061334 0L512 1012.394667zM469.333333 426.666667V298.666667h85.333334v128h128v85.333333h-128v128h-85.333334v-128H341.333333v-85.333333h128z"  /></svg>
      </action-button>
      <action-button @click="toggleTracking">
        <svg v-if="!tracking" class="svg-icon" style="width: 2em; height: 2em; vertical-align: middle;fill: currentColor;overflow: hidden;" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"><path d="M448 379.776v264.384L646.336 512 448 379.776zM416 736h-2.304a31.68 31.68 0 0 1-23.04-12.416A32.384 32.384 0 0 1 384 704V320a32.384 32.384 0 0 1 6.656-19.52 31.36 31.36 0 0 1 35.008-10.944 32.32 32.32 0 0 1 8.448 4.096l287.04 191.424A31.424 31.424 0 0 1 736 512a31.744 31.744 0 0 1-14.784 27.008l-287.104 191.36a32.256 32.256 0 0 1-18.112 5.632zM512 64C264.96 64 64 264.96 64 512s200.96 448 448 448 448-200.96 448-448-200.96-448-448-448z m0 960c-282.304 0-512-229.696-512-512 0-282.24 229.696-512 512-512s512 229.76 512 512c0 282.304-229.696 512-512 512z"  /></svg>
        <svg v-else class="svg-icon" style="width: 2em; height: 2em; vertical-align: middle;fill: currentColor;overflow: hidden;" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"><path d="M512 1024A512 512 0 1 1 512 0a512 512 0 0 1 0 1024z m0-64A448 448 0 1 0 512 64a448 448 0 0 0 0 896zM320 352a32 32 0 0 1 32-32h320a32 32 0 0 1 32 32v320a32 32 0 0 1-32 32h-320a32 32 0 0 1-32-32v-320zM384 384v256h256V384H384z"  /></svg>
      </action-button>
    </div>

    <div class="absolute top-4 sm:top-6 z-10 h-14 w-full flex gap-4 justify-center px-4" v-if="air && weather">
      <div class="bg-white shadow-md rounded-xl p-4 text-base text-gray-600 flex items-center"><span class="mr-2">Pogoda:</span><div class="w-8"><weather-icon :weather="weather" /></div></div>
      <div class="bg-white shadow-md rounded-xl p-4 text-base text-gray-600 flex items-center"><span class="mr-2">Powietrze:</span><div class="w-8"><air-icon :air="air" /></div></div>
    </div>

    <!-- Map -->
    <l-map
      v-model="zoom"
      v-model:zoom="zoom"
      :center="coords"
      :options="{ zoomControl: false }"
      class="z-0"
    >
      <l-control-zoom position="bottomright"  ></l-control-zoom>

      <l-tile-layer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      ></l-tile-layer>

      <!-- Location markers -->
      <l-marker :lat-lng="location.coords" v-for="(location, index) in locations" :key="index">
        <l-tooltip>
          {{location.tags}}
        </l-tooltip>
      </l-marker>

      <!-- Routes -->
      <l-polyline
        v-for="(route, index) in routes" :key="index"
        :lat-lngs="route.points"
        color="#083763"
      ></l-polyline>      
    </l-map>
  </div>
</template>
<script>
import {
  LMap,
  LIcon,
  LTileLayer,
  LMarker,
  LControlLayers,
  LControlZoom,
  LTooltip,
  LPopup,
  LPolyline,
} from "@vue-leaflet/vue-leaflet";
import { latLng } from 'leaflet';
import LocationModal from "./components/LocationModal.vue";
import TitleModal from "./components/TitleModal.vue";
import ActionButton from "./components/ActionButton.vue";
import AirIcon from "./components/AirIcon.vue";
import WeatherIcon from "./components/WeatherIcon.vue";
import "leaflet/dist/leaflet.css";

import { initializeApp } from "firebase/app";
import { getFirestore, collection, query, where, onSnapshot } from "firebase/firestore";
import ky from 'ky';

let locationWatcher, routeWatcher;
const firebaseConfig = {
  apiKey: "AIzaSyCIsN0BG2WedCcrAAJ3MwMtWQkOd0yuIXg",
  authDomain: "ally-hackaton.firebaseapp.com",
  projectId: "ally-hackaton",
  storageBucket: "ally-hackaton.appspot.com",
  messagingSenderId: "573564758802",
  appId: "1:573564758802:web:71ff2ee0eddd52eb0b21cb",
  measurementId: "G-RMVHBRTSH6"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);
const API_BASE = 'https://167.71.33.236:8081';

export default {
  components: {
    LocationModal,
    TitleModal,
    ActionButton,
    LMap,
    LIcon,
    LTileLayer,
    LMarker,
    LControlLayers,
    LControlZoom,
    LTooltip,
    LPopup,
    LPolyline,
    AirIcon,
    WeatherIcon
  },
  data() {
    return {
      zoom: 14, // initial zoom
      lat: 52, // initial coords
      lon: 18,
      locations: [],
      routes: [],
      title: '',
      tracking: false,
      showLocationModal: false,
      showTitleModal: true,
      initialMapZoom: false,
      air: 0,
      weather: 0
    };
  },
  computed: {
    coords() {
      return latLng(this.lat, this.lon)
    }
  },
  mounted() {
    const options = {
      enableHighAccuracy: false,
      timeout: 1000,
      maximumAge: 0
    };
    let lastLat = 0;
    let lastLng = 0;

    const getWeather = async () => {
      const data = await ky.get(API_BASE + '/weather_conditions/').json();
      this.weather = data.temperature;
      this.air = data.air_conditions;
    }
    getWeather();
    setInterval(getWeather, 30000);

    setTimeout(() => {
      navigator.geolocation.getCurrentPosition(pos => {
        this.lat = pos.coords.latitude;
        this.lon = pos.coords.longitude;
      }, err => {
        console.error(err)
        alert('Błąd podczas pobierania aktualnej pozycji, sprawdź uprawnienia.')
      }, options);

      navigator.geolocation.watchPosition(async pos => {
        if (this.tracking && pos.coords.latitude !== lastLat && pos.coords.longitude !== lastLng) {
          await ky.post(API_BASE + '/routes/', {json: {
            title: this.title,
            points: [{
              lat: pos.coords.latitude,
              lon: pos.coords.longitude,
            }],
          }});
          lastLat = pos.coords.latitude;
          lastLng = pos.coords.longitude;
        }
      }, () => {}, options)
    }, 200);
  },
  watch: {
    title() {
      if (locationWatcher) {
        locationWatcher.unsubscribe();
        routeWatcher.unsubscribe();
      }
      const locationQuery = query(collection(db, "locations"), where("title", "==", this.title)); 
      locationWatcher = onSnapshot(locationQuery, snapshot => {
        this.locations = [];
        snapshot.forEach((doc) => {
          const data = doc.data();
          this.locations.push({
            tags: data.tags,
            lat: data.lat,
            lon: data.lon,
            coords: latLng(data.lat, data.lon)
          })
        });
        if (this.locations.length > 0 && !this.initialMapZoom) {
          this.lat = this.locations[0].lat;
          this.lon = this.locations[0].lon;
          this.initialMapZoom = true;
        }
      });

      const routesQuery = query(collection(db, "routes"), where("title", "==", this.title)); 
      routeWatcher = onSnapshot(routesQuery, snapshot => {
        this.routes = [];
        snapshot.forEach((doc) => {
          const data = doc.data();
          this.routes.push({
            points: data.points.map(point => latLng(point.lat, point.lon))
          })
        });
        if (this.routes.length > 0 && this.routes[0].points.length > 0 && !this.initialMapZoom) {
          this.lat = this.routes[0].points[0].lat;
          this.lon = this.routes[0].points[0].lon;
          this.initialMapZoom = true;
        }
      });
    }
  },
  methods: {
    log(a) {
      console.log(a);
    },
    changeIcon() {
      this.iconWidth += 2;
      if (this.iconWidth > this.iconHeight) {
        this.iconWidth = Math.floor(this.iconHeight / 2);
      }
    },
    toggleTracking() {
      this.tracking = !this.tracking;
    },
    saveTitle(title) {
      this.showTitleModal = false;
      this.title = title;
    },
    async addLocation(tags) {
      try {
        await ky.post(API_BASE + '/locations/', {json: {
          lat: this.lat,
          lon: this.lon,
          title: this.title,
          tags
        }});
        this.showLocationModal = false;
      } catch (e) {
        alert("Wystąpił błąd podczas dodawania lokacji: " + e.message)
      }
    }
  },
};
</script>

<style>
  html, body {
    margin: 0;
    padding: 0;
  }
</style>