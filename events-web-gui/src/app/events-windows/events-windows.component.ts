import { Component } from '@angular/core';
import { environment } from 'src/environments/environment';
import { EventSchema, ActorSchema, RepositorySchema } from '../models';

@Component({
  selector: 'app-events-windows',
  templateUrl: './events-windows.component.html',
  styleUrls: ['./events-windows.component.css']
})
export class EventsWindowsComponent  {
  recent_events: EventSchema[] = [];

  constructor() {
    console.log('EventsWindowsComponent constructor called');
  }

  ngOnInit() {
    console.log('EventsWindowsComponent ngOnInit called');

    // Fetch the recent events, /events with the parameter limit and skip
    fetch(`${environment.backendBaseUrl}/events?limit=${20}&skip=${0}`)
      .then(response => response.json())
      .then(data => {
        console.log('Recent events:', data);
        this.recent_events = data;
      })
      .catch(error => {
        console.log('Error fetching recent events:', error);
      });
    }


}
