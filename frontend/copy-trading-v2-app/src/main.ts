import { bootstrapApplication } from '@angular/platform-browser';
import { provideRouter, Routes } from '@angular/router';
import { importProvidersFrom } from '@angular/core';
import { provideHttpClient } from '@angular/common/http';
import { ReactiveFormsModule } from '@angular/forms'; // Import ReactiveFormsModule
import { AppComponent } from './app/app.component';
import { DashboardComponent } from './app/components/dashboard/dashboard.component';
import { ListUsersComponent } from './app/components/list-users/list-users.component';
import { PlaceTradeComponent } from './app/components/place-trade/place-trade.component';
import { OrdersComponent } from './app/components/orders/orders.component';
import { TradesComponent } from './app/components/trades/trades.component';
import { NetPositionsComponent } from './app/components/net-positions/net-positions.component';
import { HoldingsComponent } from './app/components/holdings/holdings.component';
import { ModifyOrderComponent } from './app/components/modify-order/modify-order.component';
import { CancelOrderComponent } from './app/components/cancel-order/cancel-order.component';
import { SquareOffPositionComponent } from './app/components/square-off-position/square-off-position.component';
import { UserManualComponent } from './app/components/user-manual/user-manual.component';

const routes: Routes = [
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'list-users', component: ListUsersComponent },
  { path: 'place-trade', component: PlaceTradeComponent },
  { path: 'orders', component: OrdersComponent },
  { path: 'trades', component: TradesComponent },
  { path: 'net-positions', component: NetPositionsComponent },
  { path: 'holdings', component: HoldingsComponent },
  { path: 'modify-order', component: ModifyOrderComponent },
  { path: 'cancel-order', component: CancelOrderComponent },
  { path: 'square-off-position', component: SquareOffPositionComponent },
  { path: 'manual', component: UserManualComponent }
];

bootstrapApplication(AppComponent, {
  providers: [
    provideRouter(routes),
    provideHttpClient(),
    importProvidersFrom(ReactiveFormsModule) // Add ReactiveFormsModule to imports
  ]
});