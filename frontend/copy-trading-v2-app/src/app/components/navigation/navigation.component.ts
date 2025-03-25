import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-navigation',
  templateUrl: './navigation.component.html',
  styleUrls: ['../../../styles.css'],
  standalone: true,
  imports: [RouterModule]
})
export class NavigationComponent {}