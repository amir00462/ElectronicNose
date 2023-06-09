import datetime
from github import Github
import random
import time
import schedule

# amir00462
github = Github('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')
androidRepo = [
    github.get_repo('amir00462/CiCd_Points_Android'),
    github.get_repo('amir00462/DrawPad_Android'),
    github.get_repo('amir00462/FaceTime_android'),
    github.get_repo('amir00462/Drawer_androidd')
]

# dunijet
# github = Github('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')
# androidRepo = [
#     github.get_repo('dunijet/cicd_points_android'),
#     github.get_repo('dunijet/cicd_points_android'),
#     github.get_repo('dunijet/cicd_points_android'),
#     github.get_repo('dunijet/cicd_points_android'),
# ]

path = 'app/src/main/java/ir/dunijet/cicdpointsandroid/'
todayCommits = random.randint(10, 20)

def contentGenerator(name):
    content = """
    Fragment : Fragment() {
    private lateinit var textView: TextView

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        val view = inflater.inflate(R.layout.fragment_my, container, false)
        textView = view.findViewById(R.id.text_view)
        return view
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        textView.text = "Hello, World!"
    }
}
"""

    name = f'class {name}'
    return name + content
def nameGenerator():
    screens = [
        'SplashScreen',
        'LoginScreen',
        'SignUpScreen',
        'HomeScreen',
        'ProductListScreen',
        'ProductDetailScreen',
        'SearchScreen',
        'FilterScreen',
        'CartScreen',
        'CheckoutScreen',
        'PaymentScreen',
        'OrderConfirmationScreen',
        'ProfileScreen',
        'EditProfileScreen',
        'AddressBookScreen',
        'AddAddressScreen',
        'EditAddressScreen',
        'OrderHistoryScreen',
        'OrderDetailScreen',
        'ShippingInformationScreen',
        'ReturnsAndExchangesScreen',
        'SupportScreen',
        'FAQScreen',
        'AboutUsScreen',
        'ContactUsScreen',
        'NotificationsScreen',
        'PushNotificationsSettingsScreen',
        'EmailNotificationsSettingsScreen',
        'SocialMediaSharingScreen',
        'RatingAndReviewScreen',
        'WishlistScreen',
        'ProductComparisonScreen',
        'SaleScreen',
        'FeaturedProductsScreen',
        'RecommendedProductsScreen',
        'RecentlyViewedProductsScreen',
        'PopularProductsScreen',
        'NewArrivalsScreen',
        'ProductCategoriesScreen',
        'SubcategoryScreen',
        'DealsScreen',
        'CouponsScreen',
        'GiftCardsScreen',
        'ReferralProgramScreen',
        'LoyaltyProgramScreen',
        'ShippingMethodScreen',
        'PaymentMethodScreen',
        'OrderSummaryScreen',
        'TrackOrderScreen',
        'HelpCenterScreen',
        'TermsAndConditionsScreen',
        'PrivacyPolicyScreen',
        'CookiePolicyScreen',
        'GdprComplianceScreen',
        'AgeVerificationScreen',
        'StoreLocatorScreen',
        'StoreInformationScreen',
        'StoreHoursScreen',
        'FeaturedBrandsScreen',
        'BrandDetailScreen',
        'BrandProductsScreen',
        'SizeChartScreen',
        'ColorOptionsScreen',
        'ReviewsScreen',
        'WriteAReviewScreen',
        'MyRewardsScreen',
        'RedeemRewardsScreen',
        'ReferralDashboardScreen',
        'ReferralHistoryScreen',
        'ReferralSharingScreen',
        'ReferralBonusScreen',
        'ShareAppScreen',
        'AppSettingsScreen',
        'LanguageSelectionScreen',
        'CurrencySelectionScreen',
        'ThemeSelectionScreen',
        'DarkModeScreen',
        'LightModeScreen',
        'FontSelectionScreen',
        'PushNotificationPreferencesScreen',
        'EmailNotificationPreferencesScreen',
        'SmsNotificationPreferencesScreen',
        'SocialMediaAccountLinkingScreen',
        'AccountVerificationScreen',
        'EmailVerificationScreen',
        'PhoneVerificationScreen',
        'AccountDeletionScreen',
        'ForgotPasswordScreen',
        'PasswordResetScreen',
        'ChangePasswordScreen',
        'ProductImageGalleryScreen',
        'ProductVideoScreen',
        'CustomerServiceScreen',
        'ChatSupportScreen',
        'ContactFormScreen',
        'FeedbackScreen',
        'RequestACallBackScreen',
        'UserAgreementScreen',
        'TransactionHistoryScreen',
        'UserActivityScreen'
    ]

    random_screen = random.choice(screens)
    return random_screen + '_' + str(random.randint(10, 137946))

def runCode():
    todayCommits = random.randint(1, 10)

    while todayCommits > 0:
        name = nameGenerator()
        value = contentGenerator(name)
        commitCode = str(random.randint(4675197, 73491576))

        androidRepo.create_file(
            path=path + name + '.kt',
            message=name + ' added, code: ' + commitCode,
            content=value,
            branch='master'
        )

        print('new commit with id: ' + commitCode)
        time.sleep(random.randint(10, 25))
        todayCommits -= 1

def runCodeOneTime(todayCommits):
    while todayCommits > 0:
        name = nameGenerator()

        value = contentGenerator(name)
        commitCode = str(random.randint(4675197, 73491576))

        whichRepo = random.randint(0, 3)
        androidRepo[whichRepo].create_file(
            path=path + name + '.kt',
            message=name + ' added, code: ' + commitCode,
            content=value,
            branch='master'
        )

        print('new commit with id: ' + commitCode)
        time.sleep(random.randint(4, 9))
        todayCommits -= 1


def modeAlways():
    scheduleTime = random.randint(1, 3)
    schedule.every(1).minutes.do(runCode)
    print('schedule time is: ' + str(scheduleTime))

    while True:
        try:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print('\njob scheduled at ' + now)
            schedule.run_pending()
            time.sleep(30)
        except:
            print('process stoped :)')


def modeNow():
    runCodeOneTime(todayCommits)


if __name__ == '__main__':
    modeNow()
