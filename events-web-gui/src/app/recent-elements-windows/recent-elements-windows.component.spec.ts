import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RecentElementsWindowsComponent } from './recent-elements-windows.component';

describe('RecentElementsWindowsComponent', () => {
  let component: RecentElementsWindowsComponent;
  let fixture: ComponentFixture<RecentElementsWindowsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RecentElementsWindowsComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RecentElementsWindowsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
