import { Component, OnInit } from '@angular/core';
import { TradeService } from '../../services/trade.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-list-users',
  templateUrl: './list-users.component.html',
  standalone: true,
  providers: [TradeService],
  imports: [CommonModule]
})
export class ListUsersComponent implements OnInit {
  users: any[] = [];
  error: string | null = null;

  constructor(private tradeService: TradeService) {}

  ngOnInit(): void {
    this.tradeService.getUsers().subscribe(
      (data) => {
        this.users = data;
      },
      (error) => {
        this.error = 'Failed to load users';
        console.error(error);
      }
    );
  }
}