# flake8: noqa
CHATLOG = [
            { "role": "user", "content": '''
                @meal_plan_router.get('/', response=List[MealPlanListSchema],
                      url_name='meal_plans')
                def meal_plan_list(request):
                """Delete all meal plans in the system."""
                    user = request.auth
                    queryset = MealPlan.objects.filter(user=user).order_by('-creation_date')
                    return queryset


                @meal_plan_router.get('/current', response={
                                    200: MealPlanOut, 204: None},
                                    url_name='current_meal_plan')
                def get_current_meal_plan(request):
                    """Retrieve details of current meal plan which is the latest meal plan
                    that is at most a week old."""
                    user = request.auth
                    one_week_ago = datetime.now().date() - timedelta(days=7)
                    meal_plan = MealPlan.objects.filter(
                        user=user, creation_date__gte=one_week_ago).order_by(
                            '-creation_date').first()
                    if meal_plan is None:
                        return 204, None  # There are not enough meal plans
                    return meal_plan
            ''' },
            { "role": "assistant", "content": '''
                4, Retrieve all meal plans in the system.
                22, There are no meal plans.
            '''}
        ]
