import { Component, OnInit } from '@angular/core';
import { UserService } from '../../services/user.service';
import { FormBuilder, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-list-users',
  templateUrl: './list-users.component.html',
  standalone: true,
  providers: [UserService],
  imports: [ReactiveFormsModule,CommonModule]
})
export class ListUsersComponent implements OnInit {
  users: any[] = [];
  error: string | null = null;
  addUserForm: FormGroup;
  modifyUserForm: FormGroup;
  deleteUserForm: FormGroup;
  validateUserForm: FormGroup;
  currentForm: string | null = null;

  constructor(private userService: UserService, private fb: FormBuilder) {
    this.addUserForm = this.fb.group({
      userid: [''],
      active: [false],
      reqId: [''],
      username: [''],
      apiKey: [''],
      api_secret_password: [''],
      session_active: [false]
    });

    this.modifyUserForm = this.fb.group({
      userid: [''],
      active: [false],
      reqId: [''],
      username: [''],
      apiKey: [''],
      api_secret_password: [''],
      session_active: [false]
    });

    this.deleteUserForm = this.fb.group({
      userid: ['']
    });

    this.validateUserForm = this.fb.group({
      userid: ['']
    });
  }

  ngOnInit(): void {
    this.loadUsers();
  }

  loadUsers(): void {
    this.userService.getAllUsers().subscribe(
      (data) => {
        this.users = data;
        this.currentForm = null;
      },
      (error) => {
        this.error = 'Failed to load users';
        console.error(error);
      }
    );
  }

  showForm(event: Event, formName: string, user: any = null): void {
    event.preventDefault();
    this.currentForm = formName;
    this.error = null;

    if (user) {
      if (formName === 'modify') {
        this.modifyUserForm.setValue({
          userid: user.userid,
          active: user.active,
          reqId: user.reqId,
          username: user.username,
          apiKey: user.apiKey,
          api_secret_password: user.api_secret_password,
          session_active: user.session_active
        });
      } else if (formName === 'delete') {
        this.deleteUserForm.setValue({
          userid: user.userid
        });
      } else if (formName === 'validate') {
        this.validateUserForm.setValue({
          userid: user.userid
        });
      }
    }
  }

  hideForm(): void {
    this.currentForm = null;
  }

  addUser(): void {
    if (this.addUserForm.valid) {
      if (window.confirm('Are you sure you want to add this user?')) {
        this.userService.addUser(this.addUserForm.value).subscribe(
          () => {
            this.loadUsers();
            this.addUserForm.reset();
          },
          (error) => {
            this.error = 'Failed to add user';
            console.error(error);
          }
        );
        }
    }
  }

  modifyUser(): void {
    if (this.modifyUserForm.valid) {
      if(window.confirm('Are you sure you want to modify this user?')){
        this.userService.modifyUser(this.modifyUserForm.value).subscribe(
          () => {
            this.loadUsers();
            this.modifyUserForm.reset();
          },
          (error) => {
            this.error = 'Failed to modify user';
            console.error(error);
          }
        );
      }
    }
  }

  deleteUser(): void {
    if (this.deleteUserForm.valid) {
      if (window.confirm('Are you sure you want to delete this user?')) {
        this.userService.deleteUser(this.deleteUserForm.value.userid).subscribe(
          () => {
            this.loadUsers();
            this.deleteUserForm.reset();
          },
          (error) => {
            this.error = 'Failed to delete user';
            console.error(error);
          }
        );
      }
    }
  }

  validateUser(): void {
    if (this.validateUserForm.valid) {
      if(window.confirm('Are you sure you want to validate this user?')){
        this.userService.validateUser(this.validateUserForm.value.userid).subscribe(
          () => {
            this.loadUsers();
            this.validateUserForm.reset();
          },
          (error) => {
            this.error = 'Failed to validate user';
            console.error(error);
          }
        );
        }
    }
  }
}