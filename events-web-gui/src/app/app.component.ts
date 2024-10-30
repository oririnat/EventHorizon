import { Component, OnInit } from '@angular/core';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'events-web-gui';
  num_of_collected_events = 0;

  constructor() {
    console.log('AppComponent constructor called');
  }

  ngOnInit() {
    console.log('AppComponent ngOnInit called');

    // Fetch the number of collected events

    fetch(`${environment.backendBaseUrl}/events/count`)
      .then(response => response.json())
      .then(data => {
        console.log('Number of collected events:', data);
        this.num_of_collected_events = data.total_events;
      })
      .catch(error => {
        console.log('Error fetching number of collected events:', error);
      });
  }
}
