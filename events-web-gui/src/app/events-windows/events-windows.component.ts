import { AfterViewInit, Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { environment } from 'src/environments/environment';
import { EventSchema, ActorSchema, RepositorySchema } from '../models';

@Component({
  selector: 'app-events-windows',
  templateUrl: './events-windows.component.html',
  styleUrls: ['./events-windows.component.css']
})
export class EventsWindowsComponent implements OnInit {
  @Input() num_of_collected_events = 0
  @Output() reload_events: EventEmitter<any> = new EventEmitter()
  page = 1;
  num_of_pages = 1;
  events_per_page = 20;
  is_events_loading = false;
  search_term = '';

  event_types =
  [
    "All",
    "CommitCommentEvent",
    "CreateEvent",
    "DeleteEvent",
    "ForkEvent",
    "GollumEvent",
    "IssueCommentEvent",
    "IssuesEvent",
    "MemberEvent",
    "PublicEvent",
    "PullRequestEvent",
    "PullRequestReviewEvent",
    "PullRequestReviewCommentEvent",
    "PullRequestReviewThreadEvent",
    "PushEvent",
    "ReleaseEvent",
    "SponsorshipEvent",
    "WatchEvent"]

  recent_events: EventSchema[] = [];

  constructor() {
    console.log('EventsWindowsComponent constructor called');
  }

  ngOnInit() {
    console.log("num_of_collected_events: " + this.num_of_collected_events)
    this.num_of_pages = Math.ceil(this.num_of_collected_events / 20)
    console.log('EventsWindowsComponent ngOnInit called');

    this.load_events();

  }

  load_events(limit: number = 20, skip: number = 0) {
    this.is_events_loading = true;
    this.recent_events = [];
      // Fetch the recent events, /events with the parameter limit and skip
    fetch(`${environment.backendBaseUrl}/events?limit=${limit}&skip=${skip}&search_term=${this.search_term}`)
      .then(response => response.json())
      .then(data => {
        this.recent_events = data;
      })
      .catch(error => {
        console.log('Error fetching recent events:', error);
      }).finally(() => {
        this.is_events_loading = false;
      });

  }

  filterEvents(sortEvent: any) {
    this.search_term = sortEvent.target.value;
    if (this.search_term == 'All') {
      this.search_term = '';
    }
    this.load_events(this.events_per_page, 0)
  }

  search() {
      console.log('searchEvent:', this.search_term);
      this.load_events(this.events_per_page, 0)
  }

  searchEvents(searchEvent: any) {
    // If enter key is pressed
    if (searchEvent.keyCode == 13) {
      this.search();
      return;
    }
    this.search_term = searchEvent.target.value;
  }

  prevPage() {
    if (this.page > 1) {
      this.load_events(this.events_per_page, (this.page - 2) * this.events_per_page)
      this.page -= 1;
    }
  }

  nextPage() {
    if (this.page < this.get_total_num_of_pages()) {
      this.load_events(this.events_per_page, this.page * this.events_per_page)
      this.page += 1;

    }
  }

  get_total_num_of_pages(){
    return Math.ceil(this.num_of_collected_events / 20)
  }

  reloadEvents() {
    this.page = 1;
    this.reload_events.emit();
    this.load_events(this.events_per_page, 0)
  }
}
